from datetime import datetime, timedelta, timezone

from app.memory.overrides import StrategicOverride, OverrideType


def test_override_expiration() -> None:
    now = datetime.now(timezone.utc)
    override = StrategicOverride(
        override_id="o1",
        run_id="run",
        override_type=OverrideType.TOOL_BUDGET,
        constraints={"max_calls": 3},
        expires_at=now + timedelta(seconds=5),
    )

    assert override.is_expired(now) is False
    assert override.is_expired(now + timedelta(seconds=10)) is True
