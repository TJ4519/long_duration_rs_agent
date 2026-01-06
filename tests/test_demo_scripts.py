from pathlib import Path
import json
import subprocess
import sys


def test_demo_run_writes_output(tmp_path: Path) -> None:
    output_path = tmp_path / "demo.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/demo_run.py",
            "--objective",
            "test objective",
            "--output",
            str(output_path),
        ],
        check=True,
    )

    payload = json.loads(output_path.read_text())
    assert payload["objective"] == "test objective"
    assert payload["status"] == "ok"


def test_eval_script_passes(tmp_path: Path) -> None:
    golden = tmp_path / "golden.json"
    candidate = tmp_path / "candidate.json"
    golden.write_text("{\"value\": 1}\n")
    candidate.write_text("{\"value\": 1}\n")

    subprocess.run(
        [
            sys.executable,
            "scripts/eval.py",
            "--golden",
            str(golden),
            "--candidate",
            str(candidate),
        ],
        check=True,
    )
