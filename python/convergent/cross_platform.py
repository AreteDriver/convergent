"""Cross-platform integration for multi-agent coordination state portability.

Enables agents and systems running on different platforms (mobile backends,
web services, desktop applications, server processes) to participate in the
same coordination protocol seamlessly. Provides:

- Platform detection and capability advertisement
- Portable state snapshots for transferring coordination state across devices
- Session continuity across platform switches
- Platform registry with SQLite persistence

This module sits alongside the existing coordination protocol (Phase 3) and
extends it with cross-platform awareness. Each platform registers itself,
advertises its capabilities, and can export/import coordination state
snapshots for seamless handoff.
"""

from __future__ import annotations

import contextlib
import json
import logging
import platform
import sqlite3
import sys
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class PlatformType(str, Enum):
    """Classifies the runtime platform.

    Used to adapt coordination behavior based on platform constraints
    (e.g., mobile has limited storage, web has no filesystem access).
    """

    MOBILE = "mobile"
    WEB = "web"
    DESKTOP = "desktop"
    SERVER = "server"
    UNKNOWN = "unknown"


class PlatformCapability(str, Enum):
    """Capabilities a platform may advertise.

    Agents use this to determine what coordination features are
    available on a given platform.
    """

    FILESYSTEM = "filesystem"
    SQLITE = "sqlite"
    THREADING = "threading"
    SUBPROCESS = "subprocess"
    NETWORK = "network"
    PERSISTENT_STORAGE = "persistent_storage"
    GPU = "gpu"


def _utc_now_iso() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def detect_platform() -> PlatformContext:
    """Auto-detect the current platform context.

    Inspects the runtime environment to determine platform type,
    OS, Python version, and available capabilities.

    Returns:
        A PlatformContext describing the current environment.
    """
    os_name = platform.system().lower()
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    arch = platform.machine()

    # Determine platform type heuristically
    plat_type = PlatformType.UNKNOWN
    if os_name in ("linux", "darwin", "windows"):
        plat_type = PlatformType.DESKTOP
    if os_name == "linux" and "server" in platform.node().lower():
        plat_type = PlatformType.SERVER

    # Determine available capabilities
    capabilities: list[str] = []

    # Filesystem access
    capabilities.append(PlatformCapability.FILESYSTEM.value)

    # SQLite is always available in CPython
    capabilities.append(PlatformCapability.SQLITE.value)

    # Threading
    try:
        import threading  # noqa: F401

        capabilities.append(PlatformCapability.THREADING.value)
    except ImportError:
        pass

    # Subprocess
    try:
        import subprocess  # noqa: F401, S404

        capabilities.append(PlatformCapability.SUBPROCESS.value)
    except ImportError:
        pass

    # Network (socket availability)
    try:
        import socket  # noqa: F401

        capabilities.append(PlatformCapability.NETWORK.value)
    except ImportError:
        pass

    # Persistent storage (filesystem implies persistent storage)
    capabilities.append(PlatformCapability.PERSISTENT_STORAGE.value)

    return PlatformContext(
        platform_id=str(uuid.uuid4()),
        platform_type=plat_type,
        os_name=os_name,
        python_version=py_version,
        architecture=arch,
        capabilities=capabilities,
    )


@dataclass(frozen=True)
class PlatformContext:
    """Describes a platform's identity and capabilities.

    Attributes:
        platform_id: Unique identifier for this platform instance.
        platform_type: Classification of the platform (mobile, web, etc.).
        os_name: Operating system name (lowercase).
        python_version: Python version string.
        architecture: CPU architecture (e.g. "x86_64", "arm64").
        capabilities: List of capability strings this platform supports.
        registered_at: When this platform was registered (ISO 8601 UTC).
    """

    platform_id: str
    platform_type: PlatformType
    os_name: str
    python_version: str
    architecture: str
    capabilities: list[str] = field(default_factory=list)
    registered_at: str = field(default_factory=_utc_now_iso)

    def has_capability(self, capability: PlatformCapability) -> bool:
        """Check if this platform has a specific capability.

        Args:
            capability: The capability to check for.

        Returns:
            True if the platform has the capability.
        """
        return capability.value in self.capabilities

    def to_json(self) -> str:
        """Serialize to JSON string."""
        d = asdict(self)
        d["platform_type"] = self.platform_type.value
        return json.dumps(d)

    @classmethod
    def from_json(cls, data: str) -> PlatformContext:
        """Deserialize from JSON string."""
        d = json.loads(data)
        d["platform_type"] = PlatformType(d["platform_type"])
        return cls(**d)


@dataclass(frozen=True)
class StateSnapshot:
    """An immutable, portable snapshot of coordination state.

    Captures the current state of scores, markers, decisions, and signals
    in a JSON-serializable format that can be transferred between platforms.

    Attributes:
        snapshot_id: Unique identifier for this snapshot.
        source_platform_id: Platform that created the snapshot.
        source_platform_type: Type of the source platform.
        session_id: Session identifier for continuity tracking.
        scores: Agent phi scores as {agent_id: {domain: score}}.
        markers: Active stigmergy markers as list of dicts.
        decisions: Recent decisions as list of dicts.
        metadata: Arbitrary key-value metadata.
        created_at: When the snapshot was created (ISO 8601 UTC).
        format_version: Schema version for forward compatibility.
    """

    snapshot_id: str
    source_platform_id: str
    source_platform_type: str
    session_id: str
    scores: dict[str, dict[str, float]] = field(default_factory=dict)
    markers: list[dict[str, str | float | None]] = field(default_factory=list)
    decisions: list[dict[str, str]] = field(default_factory=dict)
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now_iso)
    format_version: str = "1.0"

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, data: str) -> StateSnapshot:
        """Deserialize from JSON string."""
        return cls(**json.loads(data))


_SCHEMA = """\
CREATE TABLE IF NOT EXISTS platforms (
    platform_id TEXT PRIMARY KEY,
    platform_type TEXT NOT NULL,
    os_name TEXT NOT NULL,
    python_version TEXT NOT NULL,
    architecture TEXT NOT NULL,
    capabilities TEXT NOT NULL,
    registered_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_platforms_type ON platforms(platform_type);

CREATE TABLE IF NOT EXISTS state_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    source_platform_id TEXT NOT NULL,
    source_platform_type TEXT NOT NULL,
    session_id TEXT NOT NULL,
    snapshot_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_snapshots_session ON state_snapshots(session_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_platform ON state_snapshots(source_platform_id);

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    created_by_platform TEXT NOT NULL,
    current_platform TEXT,
    state TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    last_updated TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sessions_state ON sessions(state);
"""


class CrossPlatformHub:
    """Manages cross-platform state synchronization and session continuity.

    Provides a registry of platforms, portable state snapshots, and
    session tracking so coordination state can seamlessly transfer
    between devices.

    Args:
        db_path: SQLite database path, or ":memory:" for in-memory.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def register_platform(self, context: PlatformContext) -> None:
        """Register a platform in the hub.

        Args:
            context: The platform context to register.
        """
        now = _utc_now_iso()
        self._conn.execute(
            "INSERT OR REPLACE INTO platforms "
            "(platform_id, platform_type, os_name, python_version, "
            "architecture, capabilities, registered_at, last_seen_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                context.platform_id,
                context.platform_type.value,
                context.os_name,
                context.python_version,
                context.architecture,
                json.dumps(context.capabilities),
                context.registered_at,
                now,
            ),
        )
        self._conn.commit()
        logger.info(
            "Registered platform %s (%s/%s)",
            context.platform_id,
            context.platform_type.value,
            context.os_name,
        )

    def get_platform(self, platform_id: str) -> PlatformContext | None:
        """Look up a registered platform.

        Args:
            platform_id: The platform to look up.

        Returns:
            The PlatformContext, or None if not found.
        """
        cursor = self._conn.execute(
            "SELECT * FROM platforms WHERE platform_id = ?",
            (platform_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_platform(row)

    def list_platforms(
        self,
        platform_type: PlatformType | None = None,
    ) -> list[PlatformContext]:
        """List registered platforms, optionally filtered by type.

        Args:
            platform_type: Filter by platform type. None for all.

        Returns:
            List of registered PlatformContext objects.
        """
        if platform_type is not None:
            cursor = self._conn.execute(
                "SELECT * FROM platforms WHERE platform_type = ? ORDER BY last_seen_at DESC",
                (platform_type.value,),
            )
        else:
            cursor = self._conn.execute(
                "SELECT * FROM platforms ORDER BY last_seen_at DESC"
            )
        return [self._row_to_platform(row) for row in cursor]

    def heartbeat(self, platform_id: str) -> bool:
        """Update the last-seen timestamp for a platform.

        Args:
            platform_id: The platform to update.

        Returns:
            True if the platform was found and updated, False otherwise.
        """
        now = _utc_now_iso()
        cursor = self._conn.execute(
            "UPDATE platforms SET last_seen_at = ? WHERE platform_id = ?",
            (now, platform_id),
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def create_session(self, platform_id: str) -> str:
        """Create a new coordination session.

        A session represents a continuous coordination context that
        can be transferred between platforms.

        Args:
            platform_id: The platform creating the session.

        Returns:
            The session_id.
        """
        session_id = str(uuid.uuid4())
        now = _utc_now_iso()
        self._conn.execute(
            "INSERT INTO sessions "
            "(session_id, created_by_platform, current_platform, state, "
            "created_at, last_updated) "
            "VALUES (?, ?, ?, 'active', ?, ?)",
            (session_id, platform_id, platform_id, now, now),
        )
        self._conn.commit()
        logger.info("Created session %s on platform %s", session_id, platform_id)
        return session_id

    def transfer_session(self, session_id: str, target_platform_id: str) -> bool:
        """Transfer a session to a different platform.

        This is the core of cross-platform continuity: the session
        moves from one device to another, preserving coordination context.

        Args:
            session_id: The session to transfer.
            target_platform_id: The destination platform.

        Returns:
            True if the transfer succeeded, False if session not found.
        """
        now = _utc_now_iso()
        cursor = self._conn.execute(
            "UPDATE sessions SET current_platform = ?, last_updated = ? "
            "WHERE session_id = ? AND state = 'active'",
            (target_platform_id, now, session_id),
        )
        self._conn.commit()
        if cursor.rowcount > 0:
            logger.info(
                "Transferred session %s to platform %s",
                session_id,
                target_platform_id,
            )
            return True
        return False

    def get_session(self, session_id: str) -> dict[str, str] | None:
        """Get session details.

        Args:
            session_id: The session to look up.

        Returns:
            Dict with session_id, created_by_platform, current_platform,
            state, created_at, last_updated — or None if not found.
        """
        cursor = self._conn.execute(
            "SELECT * FROM sessions WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            "session_id": row["session_id"],
            "created_by_platform": row["created_by_platform"],
            "current_platform": row["current_platform"],
            "state": row["state"],
            "created_at": row["created_at"],
            "last_updated": row["last_updated"],
        }

    def close_session(self, session_id: str) -> bool:
        """Close a session.

        Args:
            session_id: The session to close.

        Returns:
            True if the session was found and closed, False otherwise.
        """
        now = _utc_now_iso()
        cursor = self._conn.execute(
            "UPDATE sessions SET state = 'closed', last_updated = ? "
            "WHERE session_id = ? AND state = 'active'",
            (now, session_id),
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def save_snapshot(self, snapshot: StateSnapshot) -> None:
        """Persist a state snapshot for cross-platform transfer.

        Args:
            snapshot: The state snapshot to save.
        """
        self._conn.execute(
            "INSERT OR REPLACE INTO state_snapshots "
            "(snapshot_id, source_platform_id, source_platform_type, "
            "session_id, snapshot_json, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                snapshot.snapshot_id,
                snapshot.source_platform_id,
                snapshot.source_platform_type,
                snapshot.session_id,
                snapshot.to_json(),
                snapshot.created_at,
            ),
        )
        self._conn.commit()
        logger.info(
            "Saved snapshot %s for session %s from platform %s",
            snapshot.snapshot_id,
            snapshot.session_id,
            snapshot.source_platform_id,
        )

    def get_snapshot(self, snapshot_id: str) -> StateSnapshot | None:
        """Retrieve a state snapshot by ID.

        Args:
            snapshot_id: The snapshot to look up.

        Returns:
            The StateSnapshot, or None if not found.
        """
        cursor = self._conn.execute(
            "SELECT snapshot_json FROM state_snapshots WHERE snapshot_id = ?",
            (snapshot_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return StateSnapshot.from_json(row["snapshot_json"])

    def get_latest_snapshot(self, session_id: str) -> StateSnapshot | None:
        """Get the most recent snapshot for a session.

        This is the primary method for restoring state on a new platform:
        after session transfer, the target platform calls this to get
        the latest coordination state.

        Args:
            session_id: The session to get the latest snapshot for.

        Returns:
            The most recent StateSnapshot, or None if no snapshots exist.
        """
        cursor = self._conn.execute(
            "SELECT snapshot_json FROM state_snapshots "
            "WHERE session_id = ? ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return StateSnapshot.from_json(row["snapshot_json"])

    def list_snapshots(
        self,
        session_id: str | None = None,
        platform_id: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, str]]:
        """List snapshot summaries with optional filters.

        Args:
            session_id: Filter by session. None for all.
            platform_id: Filter by source platform. None for all.
            limit: Maximum results (default 50).

        Returns:
            List of dicts with snapshot_id, source_platform_id,
            source_platform_type, session_id, created_at.
        """
        clauses: list[str] = []
        params: list[str | int] = []

        if session_id is not None:
            clauses.append("session_id = ?")
            params.append(session_id)
        if platform_id is not None:
            clauses.append("source_platform_id = ?")
            params.append(platform_id)

        where = ""
        if clauses:
            where = "WHERE " + " AND ".join(clauses)

        params.append(limit)
        cursor = self._conn.execute(
            "SELECT snapshot_id, source_platform_id, source_platform_type, "  # noqa: S608
            f"session_id, created_at FROM state_snapshots {where} "
            "ORDER BY created_at DESC LIMIT ?",
            params,
        )
        return [
            {
                "snapshot_id": row["snapshot_id"],
                "source_platform_id": row["source_platform_id"],
                "source_platform_type": row["source_platform_type"],
                "session_id": row["session_id"],
                "created_at": row["created_at"],
            }
            for row in cursor
        ]

    def create_snapshot(
        self,
        platform_context: PlatformContext,
        session_id: str,
        scores: dict[str, dict[str, float]] | None = None,
        markers: list[dict[str, str | float | None]] | None = None,
        decisions: list[dict[str, str]] | None = None,
        metadata: dict[str, str] | None = None,
    ) -> StateSnapshot:
        """Create and persist a state snapshot from current coordination state.

        Convenience method that builds a StateSnapshot, assigns an ID, and
        saves it in one step.

        Args:
            platform_context: The platform creating the snapshot.
            session_id: The session this snapshot belongs to.
            scores: Agent phi scores as {agent_id: {domain: score}}.
            markers: Active stigmergy markers as list of dicts.
            decisions: Recent decisions as list of dicts.
            metadata: Arbitrary key-value metadata.

        Returns:
            The created and persisted StateSnapshot.
        """
        snapshot = StateSnapshot(
            snapshot_id=str(uuid.uuid4()),
            source_platform_id=platform_context.platform_id,
            source_platform_type=platform_context.platform_type.value,
            session_id=session_id,
            scores=scores or {},
            markers=markers or [],
            decisions=decisions or [],
            metadata=metadata or {},
        )
        self.save_snapshot(snapshot)
        return snapshot

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    def __del__(self) -> None:
        with contextlib.suppress(Exception):
            self._conn.close()

    def _row_to_platform(self, row: sqlite3.Row) -> PlatformContext:
        """Convert a database row to a PlatformContext."""
        return PlatformContext(
            platform_id=row["platform_id"],
            platform_type=PlatformType(row["platform_type"]),
            os_name=row["os_name"],
            python_version=row["python_version"],
            architecture=row["architecture"],
            capabilities=json.loads(row["capabilities"]),
            registered_at=row["registered_at"],
        )
