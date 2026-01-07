from pathlib import Path
import subprocess
import sys


def test_demo_and_eval(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    demo_output = tmp_path / "demo.json"
    metrics_output = tmp_path / "metrics.json"

    subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "demo_run.py"),
            "--objective",
            "demo objective",
            "--output",
            str(demo_output),
        ],
        check=True,
        cwd=root,
    )

    subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "eval.py"),
            "--golden",
            str(root / "eval" / "golden.json"),
            "--output",
            str(demo_output),
            "--metrics",
            str(metrics_output),
        ],
        check=True,
        cwd=root,
    )

    assert demo_output.exists()
    assert metrics_output.exists()
