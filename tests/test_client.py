"""Smoke tests for the Etymolt client."""

from datetime import datetime, timezone, timedelta

from etymolt import Etymolt


def test_construction():
    etymolt = Etymolt()
    assert etymolt is not None


def test_is_stale_old_verdict():
    old = {"issued_at": (datetime.now(timezone.utc) - timedelta(hours=25)).isoformat()}
    assert Etymolt.is_stale(old) is True  # type: ignore[arg-type]


def test_is_stale_fresh_verdict():
    fresh = {"issued_at": datetime.now(timezone.utc).isoformat()}
    assert Etymolt.is_stale(fresh) is False  # type: ignore[arg-type]


def test_is_stale_valid_until():
    past = {
        "issued_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        "valid_until": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
    }
    assert Etymolt.is_stale(past) is True  # type: ignore[arg-type]
