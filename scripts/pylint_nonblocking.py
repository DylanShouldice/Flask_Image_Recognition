from pathlib import Path
import subprocess
import sys

report = Path("pylint.txt")
targets = sys.argv[1:] or ["."]  # Staged Python files, or the project if none

with report.open("w", encoding="utf-8") as output:
    result = subprocess.run(
        [sys.executable, "-m", "pylint",
         "--rcfile=.pylintrc", "--score=y", *targets],
        stdout=output,
        stderr=subprocess.STDOUT,
        check=False,
    )

print(f"Pylint exited with {result.returncode}; see {report}")
# Exit 0 so pylint findings do not block the commit.
