from app.orchestrator import Orchestrator, StepPhase, StepState


def test_orchestrator_emits_event() -> None:
    orchestrator = Orchestrator(
        StepState(run_id="run-1", step_id=0, phase=StepPhase.COMPILE)
    )

    event = orchestrator.emit_event({"payload": True})

    assert event.run_id == "run-1"
    assert event.step_id == 0
    assert event.event_type.value == StepPhase.COMPILE.value
    assert event.payload == {"payload": True}
