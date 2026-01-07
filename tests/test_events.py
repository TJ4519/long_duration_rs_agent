from app.memory import Event, EventType


def test_event_to_dict() -> None:
    event = Event(
        run_id="run-1",
        step_id=1,
        event_type=EventType.COMPILE,
        payload={"status": "ok"},
    )

    payload = event.to_dict()

    assert payload["run_id"] == "run-1"
    assert payload["event_type"] == EventType.COMPILE
