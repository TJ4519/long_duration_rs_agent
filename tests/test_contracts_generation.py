from pathlib import Path
import subprocess
import sys


def test_generate_contracts_script_creates_outputs(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    contracts_dir = repo_root / "contracts"
    if contracts_dir.exists():
        for path in contracts_dir.iterdir():
            if path.is_file():
                path.unlink()

    result = subprocess.run(
        [sys.executable, "scripts/generate_contracts.py"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert (contracts_dir / "openapi.json").exists()
    assert (contracts_dir / "output_schema.json").exists()
    assert (contracts_dir / "prompts_manifest.json").exists()
    assert (contracts_dir / "migrations_summary.md").exists()
