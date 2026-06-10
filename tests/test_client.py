"""Smoke tests for the Etymolt client."""

from datetime import datetime, timezone, timedelta
import pytest

from etymolt import Etymolt, EtymoltError


def test_construction():
    etymolt = Etymolt()
    assert etymolt is not None


def test_is_stale_old_verdict():
    old = {"issued_at": (datetime.now(timezone.utc) - timedelta(hours=25)).isoformat()}
    assert Etymolt.is_stale(old) is True  # type: ignore[arg-type]


def test_is_stale_fresh_verdict():
    fresh = {"issued_at": datetime.now(timezone.utc).isoformat()}
    assert Etymolt.is_stale(fresh) is False  # type: ignore[arg-type]


def test_is_stale_past_valid_until():
    past = {
        "issued_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        "valid_until": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
    }
    assert Etymolt.is_stale(past) is True  # type: ignore[arg-type]


def test_is_stale_future_valid_until_no_issued_at():
    # Bug fix: was raising KeyError. Now returns False (valid window).
    fut = {"valid_until": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()}
    assert Etymolt.is_stale(fut) is False  # type: ignore[arg-type]


def test_is_stale_empty_dict_raises_etymolt_error():
    with pytest.raises(EtymoltError):
        Etymolt.is_stale({})  # type: ignore[arg-type]


def test_is_stale_malformed_valid_until_raises_etymolt_error():
    with pytest.raises(EtymoltError):
        Etymolt.is_stale({"valid_until": "not-a-date"})  # type: ignore[arg-type]


def test_is_stale_malformed_issued_at_raises_etymolt_error():
    with pytest.raises(EtymoltError):
        Etymolt.is_stale({"issued_at": "garbage"})  # type: ignore[arg-type]


def test_age_returns_timedelta():
    v = {"issued_at": (datetime.now(timezone.utc) - timedelta(seconds=10)).isoformat()}
    age = Etymolt.age(v)  # type: ignore[arg-type]
    assert isinstance(age, timedelta)
    assert age.total_seconds() >= 10


def test_age_empty_dict_raises():
    with pytest.raises(EtymoltError):
        Etymolt.age({})  # type: ignore[arg-type]
