"""SQLite persistence for phi-weighted agent scores and outcomes.

Follows the same patterns as sqlite_backend.py: WAL mode,
check_same_thread=False for concurrent reads. Uses a separate
database from the intent graph to keep concerns isolated.
"""

from __future__ import annotations

import logging
import sqlite3
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

_SCHEMA = """\
CREATE TABLE IF NOT EXISTS outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    skill_domain TEXT NOT NULL,
    outcome TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_outcomes_agent_domain
    ON outcomes(agent_id, skill_domain);

CREATE TABLE IF NOT EXISTS scores (
    agent_id TEXT NOT NULL,
    skill_domain TEXT NOT NULL,
    phi_score REAL NOT NULL,
    last_updated TEXT NOT NULL,
    PRIMARY KEY (agent_id, skill_domain)
);
"""


class ScoreStore:
    """SQLite persistence layer for agent outcomes and phi scores.

    Args:
        db_path: Path to SQLite database file, or ":memory:" for in-memory.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def record_outcome(
        self,
        agent_id: str,
        skill_domain: str,
        outcome: str,
        timestamp: str | None = None,
    ) -> None:
        """Record a task outcome for an agent in a skill domain.

        Args:
            agent_id: The agent whose outcome is being recorded.
            skill_domain: The skill domain (e.g. "code_review", "testing").
            outcome: The outcome ("approved", "rejected", "failed").
            timestamp: ISO 8601 timestamp. Defaults to now (UTC).
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
        self._conn.execute(
            "INSERT INTO outcomes (agent_id, skill_domain, outcome, timestamp) VALUES (?, ?, ?, ?)",
            (agent_id, skill_domain, outcome, timestamp),
        )
        self._conn.commit()

    def get_outcomes(
        self,
        agent_id: str,
        skill_domain: str,
    ) -> list[tuple[str, str]]:
        """Get all outcomes for an agent in a skill domain.

        Returns:
            List of (outcome, timestamp) tuples, ordered oldest first.
        """
        cursor = self._conn.execute(
            "SELECT outcome, timestamp FROM outcomes "
            "WHERE agent_id = ? AND skill_domain = ? "
            "ORDER BY timestamp ASC",
            (agent_id, skill_domain),
        )
        return [(row["outcome"], row["timestamp"]) for row in cursor]

    def get_all_domains(self, agent_id: str) -> list[str]:
        """Get all skill domains that have outcomes for an agent.

        Returns:
            List of distinct skill domain names.
        """
        cursor = self._conn.execute(
            "SELECT DISTINCT skill_domain FROM outcomes WHERE agent_id = ?",
            (agent_id,),
        )
        return [row["skill_domain"] for row in cursor]

    def save_score(
        self,
        agent_id: str,
        skill_domain: str,
        phi_score: float,
    ) -> None:
        """Save or update a computed phi score.

        Args:
            agent_id: The agent.
            skill_domain: The skill domain.
            phi_score: The computed phi score.
        """
        now = datetime.now(timezone.utc).isoformat()
        self._conn.execute(
            "INSERT OR REPLACE INTO scores (agent_id, skill_domain, phi_score, last_updated) "
            "VALUES (?, ?, ?, ?)",
            (agent_id, skill_domain, phi_score, now),
        )
        self._conn.commit()

    def get_score(self, agent_id: str, skill_domain: str) -> float | None:
        """Get the stored phi score for an agent in a skill domain.

        Returns:
            The phi score, or None if no score exists.
        """
        cursor = self._conn.execute(
            "SELECT phi_score FROM scores WHERE agent_id = ? AND skill_domain = ?",
            (agent_id, skill_domain),
        )
        row = cursor.fetchone()
        return row["phi_score"] if row else None

    def get_all_scores(self, agent_id: str) -> dict[str, float]:
        """Get all stored phi scores for an agent across all domains.

        Returns:
            Dict mapping skill_domain to phi_score.
        """
        cursor = self._conn.execute(
            "SELECT skill_domain, phi_score FROM scores WHERE agent_id = ?",
            (agent_id,),
        )
        return {row["skill_domain"]: row["phi_score"] for row in cursor}

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()
