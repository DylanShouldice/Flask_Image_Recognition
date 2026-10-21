"""Run Pylint from the project root with the local score threshold."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "pylint.txt"
COMMAND = [
    sys.executable,
    "-m",
    "pylint",
    f"--rcfile={ROOT / '.pylintrc'}",
    "--score=y",
    "--fail-under=9.5",
    ".",
]

with REPORT.open("w", encoding="utf-8") as output:
    result = subprocess.run(
        COMMAND, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT, check=False
    )

for line in REPORT.read_text(encoding="utf-8").splitlines():
    if line.startswith("Your code has been rated at"):
        print(line)

print(f"Pylint exited with {result.returncode}; see {REPORT}")
raise SystemExit(result.returncode)
