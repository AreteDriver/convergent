"""Tests for convergent.cross_platform cross-platform integration."""

from __future__ import annotations

import pytest
from convergent.cross_platform import (
    CrossPlatformHub,
    PlatformCapability,
    PlatformContext,
    PlatformType,
    StateSnapshot,
    detect_platform,
)

# --- PlatformType enum ---


class TestPlatformType:
    def test_values(self) -> None:
        assert PlatformType.MOBILE == "mobile"
        assert PlatformType.WEB == "web"
        assert PlatformType.DESKTOP == "desktop"
        assert PlatformType.SERVER == "server"
        assert PlatformType.UNKNOWN == "unknown"

    def test_from_string(self) -> None:
        assert PlatformType("desktop") is PlatformType.DESKTOP

    def test_all_members(self) -> None:
        assert len(PlatformType) == 5


# --- PlatformCapability enum ---


class TestPlatformCapability:
    def test_values(self) -> None:
        assert PlatformCapability.FILESYSTEM == "filesystem"
        assert PlatformCapability.SQLITE == "sqlite"
        assert PlatformCapability.THREADING == "threading"

    def test_all_members(self) -> None:
        assert len(PlatformCapability) == 7


# --- PlatformContext ---


class TestPlatformContext:
    def test_creation(self) -> None:
        ctx = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
            capabilities=["filesystem", "sqlite"],
        )
        assert ctx.platform_id == "plat-1"
        assert ctx.platform_type == PlatformType.DESKTOP
        assert ctx.os_name == "linux"
        assert ctx.python_version == "3.11.0"
        assert ctx.architecture == "x86_64"

    def test_has_capability(self) -> None:
        ctx = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
            capabilities=["filesystem", "sqlite"],
        )
        assert ctx.has_capability(PlatformCapability.FILESYSTEM) is True
        assert ctx.has_capability(PlatformCapability.SQLITE) is True
        assert ctx.has_capability(PlatformCapability.GPU) is False

    def test_json_round_trip(self) -> None:
        ctx = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.SERVER,
            os_name="linux",
            python_version="3.10.0",
            architecture="arm64",
            capabilities=["filesystem", "threading"],
        )
        json_str = ctx.to_json()
        restored = PlatformContext.from_json(json_str)
        assert restored.platform_id == ctx.platform_id
        assert restored.platform_type == ctx.platform_type
        assert restored.os_name == ctx.os_name
        assert restored.capabilities == ctx.capabilities

    def test_frozen(self) -> None:
        ctx = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
        )
        with pytest.raises(AttributeError):
            ctx.platform_id = "new-id"  # type: ignore[misc]

    def test_default_capabilities_empty(self) -> None:
        ctx = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.UNKNOWN,
            os_name="unknown",
            python_version="3.10.0",
            architecture="unknown",
        )
        assert ctx.capabilities == []


# --- StateSnapshot ---


class TestStateSnapshot:
    def test_creation(self) -> None:
        snap = StateSnapshot(
            snapshot_id="snap-1",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
            scores={"agent-1": {"code_review": 0.8}},
            markers=[{"target": "src/auth.py", "type": "file_modified"}],
            decisions=[{"outcome": "approved"}],
            metadata={"project": "test"},
        )
        assert snap.snapshot_id == "snap-1"
        assert snap.scores == {"agent-1": {"code_review": 0.8}}
        assert snap.format_version == "1.0"

    def test_json_round_trip(self) -> None:
        snap = StateSnapshot(
            snapshot_id="snap-1",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
            scores={"agent-1": {"code_review": 0.8}},
            metadata={"key": "value"},
        )
        json_str = snap.to_json()
        restored = StateSnapshot.from_json(json_str)
        assert restored.snapshot_id == snap.snapshot_id
        assert restored.scores == snap.scores
        assert restored.metadata == snap.metadata
        assert restored.format_version == "1.0"

    def test_frozen(self) -> None:
        snap = StateSnapshot(
            snapshot_id="snap-1",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
        )
        with pytest.raises(AttributeError):
            snap.snapshot_id = "new"  # type: ignore[misc]

    def test_default_empty_collections(self) -> None:
        snap = StateSnapshot(
            snapshot_id="snap-1",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
        )
        assert snap.scores == {}
        assert snap.markers == []
        assert snap.metadata == {}


# --- detect_platform ---


class TestDetectPlatform:
    def test_returns_platform_context(self) -> None:
        ctx = detect_platform()
        assert isinstance(ctx, PlatformContext)
        assert ctx.platform_id  # Non-empty UUID
        assert ctx.os_name  # Non-empty OS name
        assert ctx.python_version  # Non-empty version
        assert ctx.architecture  # Non-empty arch

    def test_capabilities_include_basics(self) -> None:
        ctx = detect_platform()
        assert PlatformCapability.FILESYSTEM.value in ctx.capabilities
        assert PlatformCapability.SQLITE.value in ctx.capabilities

    def test_unique_platform_ids(self) -> None:
        ctx1 = detect_platform()
        ctx2 = detect_platform()
        assert ctx1.platform_id != ctx2.platform_id

    def test_platform_type_is_set(self) -> None:
        ctx = detect_platform()
        assert ctx.platform_type in list(PlatformType)


# --- CrossPlatformHub ---


class TestCrossPlatformHubPlatforms:
    def test_register_and_get_platform(self) -> None:
        hub = CrossPlatformHub(":memory:")
        ctx = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
            capabilities=["filesystem", "sqlite"],
        )
        hub.register_platform(ctx)
        retrieved = hub.get_platform("plat-1")
        assert retrieved is not None
        assert retrieved.platform_id == "plat-1"
        assert retrieved.platform_type == PlatformType.DESKTOP
        assert retrieved.capabilities == ["filesystem", "sqlite"]

    def test_get_nonexistent_platform(self) -> None:
        hub = CrossPlatformHub(":memory:")
        assert hub.get_platform("nonexistent") is None

    def test_list_platforms(self) -> None:
        hub = CrossPlatformHub(":memory:")
        hub.register_platform(PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
        ))
        hub.register_platform(PlatformContext(
            platform_id="plat-2",
            platform_type=PlatformType.MOBILE,
            os_name="android",
            python_version="3.11.0",
            architecture="arm64",
        ))
        platforms = hub.list_platforms()
        assert len(platforms) == 2

    def test_list_platforms_by_type(self) -> None:
        hub = CrossPlatformHub(":memory:")
        hub.register_platform(PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
        ))
        hub.register_platform(PlatformContext(
            platform_id="plat-2",
            platform_type=PlatformType.MOBILE,
            os_name="android",
            python_version="3.11.0",
            architecture="arm64",
        ))
        desktops = hub.list_platforms(PlatformType.DESKTOP)
        assert len(desktops) == 1
        assert desktops[0].platform_id == "plat-1"

    def test_list_platforms_empty(self) -> None:
        hub = CrossPlatformHub(":memory:")
        assert hub.list_platforms() == []

    def test_heartbeat_updates_last_seen(self) -> None:
        hub = CrossPlatformHub(":memory:")
        ctx = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
        )
        hub.register_platform(ctx)
        assert hub.heartbeat("plat-1") is True

    def test_heartbeat_nonexistent(self) -> None:
        hub = CrossPlatformHub(":memory:")
        assert hub.heartbeat("nonexistent") is False

    def test_register_overwrites_existing(self) -> None:
        hub = CrossPlatformHub(":memory:")
        ctx1 = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.10.0",
            architecture="x86_64",
        )
        hub.register_platform(ctx1)
        ctx2 = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.SERVER,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
        )
        hub.register_platform(ctx2)
        retrieved = hub.get_platform("plat-1")
        assert retrieved is not None
        assert retrieved.platform_type == PlatformType.SERVER
        assert retrieved.python_version == "3.11.0"


class TestCrossPlatformHubSessions:
    def test_create_session(self) -> None:
        hub = CrossPlatformHub(":memory:")
        session_id = hub.create_session("plat-1")
        assert session_id  # Non-empty UUID
        session = hub.get_session(session_id)
        assert session is not None
        assert session["created_by_platform"] == "plat-1"
        assert session["current_platform"] == "plat-1"
        assert session["state"] == "active"

    def test_get_nonexistent_session(self) -> None:
        hub = CrossPlatformHub(":memory:")
        assert hub.get_session("nonexistent") is None

    def test_transfer_session(self) -> None:
        hub = CrossPlatformHub(":memory:")
        session_id = hub.create_session("plat-1")
        assert hub.transfer_session(session_id, "plat-2") is True
        session = hub.get_session(session_id)
        assert session is not None
        assert session["current_platform"] == "plat-2"
        assert session["created_by_platform"] == "plat-1"

    def test_transfer_nonexistent_session(self) -> None:
        hub = CrossPlatformHub(":memory:")
        assert hub.transfer_session("nonexistent", "plat-2") is False

    def test_transfer_closed_session_fails(self) -> None:
        hub = CrossPlatformHub(":memory:")
        session_id = hub.create_session("plat-1")
        hub.close_session(session_id)
        assert hub.transfer_session(session_id, "plat-2") is False

    def test_close_session(self) -> None:
        hub = CrossPlatformHub(":memory:")
        session_id = hub.create_session("plat-1")
        assert hub.close_session(session_id) is True
        session = hub.get_session(session_id)
        assert session is not None
        assert session["state"] == "closed"

    def test_close_nonexistent_session(self) -> None:
        hub = CrossPlatformHub(":memory:")
        assert hub.close_session("nonexistent") is False

    def test_close_already_closed(self) -> None:
        hub = CrossPlatformHub(":memory:")
        session_id = hub.create_session("plat-1")
        hub.close_session(session_id)
        assert hub.close_session(session_id) is False

    def test_multiple_sessions(self) -> None:
        hub = CrossPlatformHub(":memory:")
        s1 = hub.create_session("plat-1")
        s2 = hub.create_session("plat-1")
        assert s1 != s2
        assert hub.get_session(s1) is not None
        assert hub.get_session(s2) is not None


class TestCrossPlatformHubSnapshots:
    def test_save_and_get_snapshot(self) -> None:
        hub = CrossPlatformHub(":memory:")
        snap = StateSnapshot(
            snapshot_id="snap-1",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
            scores={"agent-1": {"code_review": 0.8}},
        )
        hub.save_snapshot(snap)
        retrieved = hub.get_snapshot("snap-1")
        assert retrieved is not None
        assert retrieved.snapshot_id == "snap-1"
        assert retrieved.scores == {"agent-1": {"code_review": 0.8}}

    def test_get_nonexistent_snapshot(self) -> None:
        hub = CrossPlatformHub(":memory:")
        assert hub.get_snapshot("nonexistent") is None

    def test_get_latest_snapshot(self) -> None:
        hub = CrossPlatformHub(":memory:")
        hub.save_snapshot(StateSnapshot(
            snapshot_id="snap-1",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
            metadata={"order": "first"},
            created_at="2024-01-01T00:00:00+00:00",
        ))
        hub.save_snapshot(StateSnapshot(
            snapshot_id="snap-2",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
            metadata={"order": "second"},
            created_at="2024-01-02T00:00:00+00:00",
        ))
        latest = hub.get_latest_snapshot("session-1")
        assert latest is not None
        assert latest.snapshot_id == "snap-2"
        assert latest.metadata == {"order": "second"}

    def test_get_latest_snapshot_empty(self) -> None:
        hub = CrossPlatformHub(":memory:")
        assert hub.get_latest_snapshot("nonexistent") is None

    def test_list_snapshots(self) -> None:
        hub = CrossPlatformHub(":memory:")
        hub.save_snapshot(StateSnapshot(
            snapshot_id="snap-1",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
        ))
        hub.save_snapshot(StateSnapshot(
            snapshot_id="snap-2",
            source_platform_id="plat-2",
            source_platform_type="mobile",
            session_id="session-1",
        ))
        snapshots = hub.list_snapshots()
        assert len(snapshots) == 2

    def test_list_snapshots_by_session(self) -> None:
        hub = CrossPlatformHub(":memory:")
        hub.save_snapshot(StateSnapshot(
            snapshot_id="snap-1",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
        ))
        hub.save_snapshot(StateSnapshot(
            snapshot_id="snap-2",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-2",
        ))
        s1_snaps = hub.list_snapshots(session_id="session-1")
        assert len(s1_snaps) == 1
        assert s1_snaps[0]["snapshot_id"] == "snap-1"

    def test_list_snapshots_by_platform(self) -> None:
        hub = CrossPlatformHub(":memory:")
        hub.save_snapshot(StateSnapshot(
            snapshot_id="snap-1",
            source_platform_id="plat-1",
            source_platform_type="desktop",
            session_id="session-1",
        ))
        hub.save_snapshot(StateSnapshot(
            snapshot_id="snap-2",
            source_platform_id="plat-2",
            source_platform_type="mobile",
            session_id="session-1",
        ))
        p2_snaps = hub.list_snapshots(platform_id="plat-2")
        assert len(p2_snaps) == 1
        assert p2_snaps[0]["source_platform_id"] == "plat-2"

    def test_list_snapshots_limit(self) -> None:
        hub = CrossPlatformHub(":memory:")
        for i in range(5):
            hub.save_snapshot(StateSnapshot(
                snapshot_id=f"snap-{i}",
                source_platform_id="plat-1",
                source_platform_type="desktop",
                session_id="session-1",
            ))
        snapshots = hub.list_snapshots(limit=3)
        assert len(snapshots) == 3

    def test_create_snapshot_convenience(self) -> None:
        hub = CrossPlatformHub(":memory:")
        ctx = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
        )
        session_id = hub.create_session("plat-1")
        snap = hub.create_snapshot(
            platform_context=ctx,
            session_id=session_id,
            scores={"agent-1": {"review": 0.9}},
            metadata={"project": "test"},
        )
        assert snap.source_platform_id == "plat-1"
        assert snap.scores == {"agent-1": {"review": 0.9}}
        # Should be persisted
        retrieved = hub.get_snapshot(snap.snapshot_id)
        assert retrieved is not None
        assert retrieved.scores == snap.scores


class TestCrossPlatformHubPersistence:
    def test_file_persistence(self, tmp_path: object) -> None:
        import pathlib

        db_path = str(pathlib.Path(str(tmp_path)) / "cross_platform.db")
        hub1 = CrossPlatformHub(db_path)
        ctx = PlatformContext(
            platform_id="plat-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
        )
        hub1.register_platform(ctx)
        session_id = hub1.create_session("plat-1")
        hub1.create_snapshot(
            platform_context=ctx,
            session_id=session_id,
            scores={"agent-1": {"review": 0.8}},
        )
        hub1.close()

        hub2 = CrossPlatformHub(db_path)
        assert hub2.get_platform("plat-1") is not None
        assert hub2.get_session(session_id) is not None
        snap = hub2.get_latest_snapshot(session_id)
        assert snap is not None
        assert snap.scores == {"agent-1": {"review": 0.8}}
        hub2.close()


class TestCrossPlatformHubClose:
    def test_close_prevents_operations(self) -> None:
        hub = CrossPlatformHub(":memory:")
        hub.close()
        with pytest.raises(Exception):  # noqa: B017
            hub.create_session("plat-1")


class TestCrossPlatformEndToEnd:
    def test_full_workflow(self) -> None:
        """Test the complete cross-platform handoff workflow."""
        hub = CrossPlatformHub(":memory:")

        # Register two platforms
        desktop = PlatformContext(
            platform_id="desktop-1",
            platform_type=PlatformType.DESKTOP,
            os_name="linux",
            python_version="3.11.0",
            architecture="x86_64",
            capabilities=["filesystem", "sqlite", "threading"],
        )
        mobile = PlatformContext(
            platform_id="mobile-1",
            platform_type=PlatformType.MOBILE,
            os_name="android",
            python_version="3.11.0",
            architecture="arm64",
            capabilities=["sqlite", "network"],
        )
        hub.register_platform(desktop)
        hub.register_platform(mobile)

        # Create session on desktop
        session_id = hub.create_session("desktop-1")

        # Save state on desktop
        hub.create_snapshot(
            platform_context=desktop,
            session_id=session_id,
            scores={"agent-1": {"code_review": 0.85, "testing": 0.72}},
            markers=[{"target": "src/auth.py", "type": "file_modified"}],
            metadata={"project": "my-app", "branch": "feature/auth"},
        )

        # Transfer session to mobile
        assert hub.transfer_session(session_id, "mobile-1") is True

        # Restore state on mobile
        restored = hub.get_latest_snapshot(session_id)
        assert restored is not None
        assert restored.scores["agent-1"]["code_review"] == 0.85
        assert restored.metadata["project"] == "my-app"

        # Verify session ownership changed
        session = hub.get_session(session_id)
        assert session is not None
        assert session["current_platform"] == "mobile-1"

        # Close session
        hub.close_session(session_id)
        session = hub.get_session(session_id)
        assert session is not None
        assert session["state"] == "closed"


class TestPublicAPI:
    def test_import_from_convergent(self) -> None:
        import convergent

        assert hasattr(convergent, "CrossPlatformHub")
        assert hasattr(convergent, "PlatformContext")
        assert hasattr(convergent, "PlatformType")
        assert hasattr(convergent, "PlatformCapability")
        assert hasattr(convergent, "StateSnapshot")

    def test_all_exports_listed(self) -> None:
        import convergent

        assert "CrossPlatformHub" in convergent.__all__
        assert "PlatformContext" in convergent.__all__
        assert "PlatformType" in convergent.__all__
        assert "PlatformCapability" in convergent.__all__
        assert "StateSnapshot" in convergent.__all__
