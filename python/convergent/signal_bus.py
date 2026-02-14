"""Lightweight pub/sub signal bus for inter-agent communication.

Filesystem-based: signals are written as JSON files to a signals directory.
Polling-based consumption with configurable interval. Thread-safe publish
and subscribe.

Signals are how agents say: "I'm blocked on X", "I finished Y, you can
start Z", "I found a conflict in file W."
"""

from __future__ import annotations

import json
import logging
import threading
import time
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

from convergent.protocol import Signal

logger = logging.getLogger(__name__)

# Type alias for signal callbacks
_Callback = Callable[[Signal], None]


class _SubscriberEntry:
    """Internal subscriber entry with optional agent filter.

    Attributes:
        callback: The callback function.
        agent_id: If set, only deliver targeted signals to this agent.
    """

    __slots__ = ("callback", "agent_id")

    def __init__(self, callback: _Callback, agent_id: str | None = None) -> None:
        self.callback = callback
        self.agent_id = agent_id


class SignalBus:
    """Pub/sub signal bus backed by filesystem.

    Signals are stored as JSON files in a directory. Subscribers register
    callbacks for specific signal types. A polling thread reads new signals
    and dispatches to matching subscribers.

    Args:
        signals_dir: Directory to store signal files.
        poll_interval: Seconds between polling cycles.
    """

    def __init__(self, signals_dir: Path, poll_interval: float = 1.0) -> None:
        self._signals_dir = Path(signals_dir)
        self._signals_dir.mkdir(parents=True, exist_ok=True)
        self._poll_interval = poll_interval
        self._subscribers: dict[str, list[_SubscriberEntry]] = {}
        self._lock = threading.Lock()
        self._polling = False
        self._poll_thread: threading.Thread | None = None
        # Track processed files to avoid redelivery
        self._processed: set[str] = set()

    def publish(self, signal: Signal) -> None:
        """Publish a signal to the bus.

        Writes a JSON file to the signals directory.

        Args:
            signal: The signal to publish.
        """
        # Filename: {timestamp}_{signal_type}_{source_agent}.json
        # Replace colons in timestamp for filesystem safety
        safe_ts = signal.timestamp.replace(":", "-").replace("+", "p")
        filename = f"{safe_ts}_{signal.signal_type}_{signal.source_agent}.json"
        filepath = self._signals_dir / filename
        filepath.write_text(signal.to_json(), encoding="utf-8")
        logger.info(
            "Published signal %s from %s (target=%s)",
            signal.signal_type,
            signal.source_agent,
            signal.target_agent or "broadcast",
        )

    def subscribe(
        self,
        signal_type: str,
        callback: _Callback,
        agent_id: str | None = None,
    ) -> None:
        """Subscribe to signals of a specific type.

        Args:
            signal_type: The signal type to listen for.
            callback: Function called with matching Signal objects.
            agent_id: If set, only receive signals targeted to this agent
                or broadcast signals. If None, receive all matching signals.
        """
        with self._lock:
            if signal_type not in self._subscribers:
                self._subscribers[signal_type] = []
            self._subscribers[signal_type].append(
                _SubscriberEntry(callback=callback, agent_id=agent_id)
            )
        logger.debug(
            "Subscribed to %s (agent_id=%s)",
            signal_type,
            agent_id or "any",
        )

    def unsubscribe(self, signal_type: str, callback: _Callback) -> bool:
        """Remove a callback subscription.

        Args:
            signal_type: The signal type to unsubscribe from.
            callback: The callback to remove.

        Returns:
            True if the callback was found and removed, False otherwise.
        """
        with self._lock:
            entries = self._subscribers.get(signal_type, [])
            for i, entry in enumerate(entries):
                if entry.callback is callback:
                    entries.pop(i)
                    return True
        return False

    def start_polling(self) -> None:
        """Start the background polling thread.

        Reads new signal files and dispatches to matching subscribers.
        Call stop_polling() to stop.

        Raises:
            RuntimeError: If polling is already active.
        """
        if self._polling:
            raise RuntimeError("Polling is already active")
        self._polling = True
        self._poll_thread = threading.Thread(
            target=self._poll_loop, daemon=True, name="signal-bus-poll"
        )
        self._poll_thread.start()
        logger.info("Signal bus polling started (interval=%.1fs)", self._poll_interval)

    def stop_polling(self) -> None:
        """Stop the background polling thread."""
        self._polling = False
        if self._poll_thread is not None:
            self._poll_thread.join(timeout=self._poll_interval * 2)
            self._poll_thread = None
        logger.info("Signal bus polling stopped")

    def poll_once(self) -> list[Signal]:
        """Poll for new signals once (synchronous).

        Reads unprocessed signal files, dispatches to subscribers,
        and returns the signals found.

        Returns:
            List of new signals found during this poll cycle.
        """
        new_signals = []
        signal_files = sorted(self._signals_dir.glob("*.json"))

        for filepath in signal_files:
            fname = filepath.name
            if fname in self._processed:
                continue

            try:
                raw = filepath.read_text(encoding="utf-8")
                signal = Signal.from_json(raw)
            except (json.JSONDecodeError, TypeError, KeyError):
                logger.warning("Skipping malformed signal file: %s", fname)
                self._processed.add(fname)
                continue

            self._processed.add(fname)
            new_signals.append(signal)
            self._dispatch(signal)

        return new_signals

    def get_signals(
        self,
        signal_type: str | None = None,
        since: datetime | None = None,
        source_agent: str | None = None,
    ) -> list[Signal]:
        """Read signals from the directory, optionally filtered.

        Args:
            signal_type: Filter by signal type. None for all.
            since: Only return signals after this time. None for all.
            source_agent: Filter by source agent. None for all.

        Returns:
            List of matching signals, ordered by timestamp.
        """
        signals = []
        for filepath in sorted(self._signals_dir.glob("*.json")):
            try:
                raw = filepath.read_text(encoding="utf-8")
                signal = Signal.from_json(raw)
            except (json.JSONDecodeError, TypeError, KeyError):
                continue

            if signal_type is not None and signal.signal_type != signal_type:
                continue
            if source_agent is not None and signal.source_agent != source_agent:
                continue
            if since is not None:
                sig_time = datetime.fromisoformat(signal.timestamp)
                if sig_time.tzinfo is None:
                    sig_time = sig_time.replace(tzinfo=timezone.utc)
                if sig_time <= since:
                    continue

            signals.append(signal)

        return signals

    def cleanup_expired(self, max_age_seconds: int = 3600) -> int:
        """Remove signal files older than max_age_seconds.

        Args:
            max_age_seconds: Maximum age in seconds before deletion.

        Returns:
            Count of files deleted.
        """
        now = datetime.now(timezone.utc)
        deleted = 0

        for filepath in self._signals_dir.glob("*.json"):
            try:
                raw = filepath.read_text(encoding="utf-8")
                signal = Signal.from_json(raw)
                sig_time = datetime.fromisoformat(signal.timestamp)
                if sig_time.tzinfo is None:
                    sig_time = sig_time.replace(tzinfo=timezone.utc)
                age = (now - sig_time).total_seconds()
                if age > max_age_seconds:
                    filepath.unlink()
                    self._processed.discard(filepath.name)
                    deleted += 1
            except (json.JSONDecodeError, TypeError, KeyError, OSError):
                continue

        if deleted:
            logger.info("Cleaned up %d expired signals", deleted)
        return deleted

    def clear(self) -> int:
        """Remove all signal files and reset processed set.

        Returns:
            Count of files deleted.
        """
        deleted = 0
        for filepath in self._signals_dir.glob("*.json"):
            try:
                filepath.unlink()
                deleted += 1
            except OSError:
                continue
        self._processed.clear()
        return deleted

    @property
    def is_polling(self) -> bool:
        """Whether the polling thread is active."""
        return self._polling

    def _poll_loop(self) -> None:
        """Background polling loop."""
        while self._polling:
            try:
                self.poll_once()
            except Exception:
                logger.exception("Error during signal bus poll cycle")
            time.sleep(self._poll_interval)

    def _dispatch(self, signal: Signal) -> None:
        """Dispatch a signal to matching subscribers."""
        with self._lock:
            entries = list(self._subscribers.get(signal.signal_type, []))

        for entry in entries:
            # Filter by target: deliver if broadcast, or if targeted to subscriber
            if (
                signal.target_agent is not None
                and entry.agent_id is not None
                and signal.target_agent != entry.agent_id
            ):
                continue
            try:
                entry.callback(signal)
            except Exception:
                logger.exception("Error in signal subscriber for %s", signal.signal_type)
