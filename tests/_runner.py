import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

RESULT_PREFIX = "PYCSP3_TEST_RESULT="


def run_model_file(model_file: str, timeout: int = 120):
    repo_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="pycsp3_test_") as workdir:
        script_path = str((repo_root / model_file).resolve())

        process = subprocess.run(
            [sys.executable, script_path],
            cwd=workdir,
            text=True,
            capture_output=True,
            timeout=timeout,
            env={
                **os.environ,
                "PYTHONPATH": str(repo_root)
                if not os.environ.get("PYTHONPATH")
                else str(repo_root) + os.pathsep + os.environ["PYTHONPATH"],
            },
        )

    if process.returncode != 0:
        raise AssertionError(
            "Model script failed with return code {}\nSTDOUT:\n{}\nSTDERR:\n{}".format(
                process.returncode, process.stdout, process.stderr
            )
        )

    for line in reversed(process.stdout.splitlines()):
        if line.startswith(RESULT_PREFIX):
            return json.loads(line[len(RESULT_PREFIX):])

    raise AssertionError(
        "No structured test result found in stdout.\nSTDOUT:\n{}\nSTDERR:\n{}".format(
            process.stdout, process.stderr
        )
    )
