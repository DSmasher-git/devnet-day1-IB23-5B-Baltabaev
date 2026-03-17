import os
import subprocess
import json
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "day3"
SCHEMA = ROOT / "schemas" / "day3_summary.schema.json"


def test_day3():
    env = os.environ.copy()
    assert env.get("STUDENT_TOKEN")
    assert env.get("STUDENT_NAME")
    assert env.get("STUDENT_GROUP")

    cmd = ["python", "src/day3_library_lab.py"]

    if (ART / "summary.json").exists():
        cmd.append("--offline")

    result = subprocess.run(cmd, cwd=str(ROOT), env=env)

    assert result.returncode == 0

    assert (ART / "summary.json").exists()

    summary = json.loads((ART / "summary.json").read_text())

    schema = json.loads(SCHEMA.read_text())
    jsonschema.validate(summary, schema)