from pathlib import Path
import subprocess
import sys


def test_generate_contracts_script(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, str(root / "scripts" / "generate_contracts.py")],
        check=True,
        cwd=root,
    )

    contracts_dir = root / "contracts"
    assert (contracts_dir / "openapi.json").exists()
    assert (contracts_dir / "prompts_manifest.json").exists()
    assert (contracts_dir / "output_schema.json").exists()
    assert (contracts_dir / "migrations_summary.md").exists()
