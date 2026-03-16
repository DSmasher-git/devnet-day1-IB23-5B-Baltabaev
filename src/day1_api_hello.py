#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from typing import Tuple, List

import requests

API_URL_DEFAULT = "https://jsonplaceholder.typicode.com/todos/1"
ART_DIR = "artifacts/day1"
RESPONSE_PATH = f"{ART_DIR}/response.json"
SUMMARY_PATH = f"{ART_DIR}/summary.json"
LOG_PATH = f"{ART_DIR}/run.log"

EXPECTED = {
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": False,
}

SUMMARY_SCHEMA_VERSION = "1.0"


def log(msg: str) -> None:
    os.makedirs(ART_DIR, exist_ok=True)
    line = f"{datetime.now(timezone.utc).isoformat()}Z {msg}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def dump_json_deterministic(obj: dict, path: str) -> str:
    text = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_payload(payload: dict) -> Tuple[bool, List[str]]:
    errors = []

    for k, v in EXPECTED.items():
        if k not in payload:
            errors.append(f"missing_key:{k}")
        elif payload[k] != v:
            errors.append(f"bad_value:{k}")

    return (len(errors) == 0), errors


def fetch_online(url: str, timeout: int = 10) -> Tuple[int, dict]:
    r = requests.get(url, timeout=timeout)
    return r.status_code, r.json()


def build_summary(student_token: str,
                  student_name: str,
                  student_group: str,
                  url: str,
                  status_code: int,
                  validation_passed: bool,
                  validation_errors: List[str],
                  response_sha256: str) -> dict:

    return {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "student": {
            "token": student_token,
            "name": student_name,
            "group": student_group,
        },
        "api": {
            "url": url,
            "status_code": status_code,
            "validation_passed": validation_passed,
            "validation_errors": validation_errors,
            "response_sha256": response_sha256,
        },
        "run": {
            "python": sys.version.split()[0],
            "platform": sys.platform,
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=API_URL_DEFAULT)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    os.makedirs(ART_DIR, exist_ok=True)

    student_token = os.getenv("STUDENT_TOKEN", "")
    student_name = os.getenv("STUDENT_NAME", "")
    student_group = os.getenv("STUDENT_GROUP", "")

    if not student_token or not student_name or not student_group:
        print("ERROR: Environment variables not set.", file=sys.stderr)
        return 3

    try:
        if args.offline:
            payload = load_json(RESPONSE_PATH)
            status_code = 200
            log("OFFLINE mode")
        else:
            log(f"ONLINE mode: GET {args.url}")
            status_code, payload = fetch_online(args.url)
            dump_json_deterministic(payload, RESPONSE_PATH)

        ok, errors = validate_payload(payload)

        with open(RESPONSE_PATH, "r", encoding="utf-8") as f:
            response_text = f.read()

        resp_sha = sha256_text(response_text)

        summary = build_summary(
            student_token,
            student_name,
            student_group,
            args.url,
            status_code,
            ok,
            errors,
            resp_sha
        )

        dump_json_deterministic(summary, SUMMARY_PATH)

        print(json.dumps(summary, ensure_ascii=False, indent=2))
        log("DONE")

        return 0 if ok else 2

    except Exception as e:
        log(f"ERROR: {e}")
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())