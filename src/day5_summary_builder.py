"""
Day 5 Summary Builder
Reads artifacts offline and builds summary.json
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).parent.parent
ARTIFACTS = BASE / "artifacts" / "day5"
SCHEMAS = BASE / "schemas"
SUMMARY_PATH = ARTIFACTS / "summary.json"


def get_env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def sha256_file(path: Path) -> str:
    """Return SHA-256 hex of file content, or empty string if missing."""
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def token_hash8() -> str:
    token = get_env("STUDENT_TOKEN")
    return hashlib.sha256(token.encode()).hexdigest()[:8]


def check_yang() -> dict:
    tree = ARTIFACTS / "yang" / "pyang_tree.txt"
    yang = ARTIFACTS / "yang" / "ietf-interfaces.yang"
    tree_ok = False
    if tree.exists():
        content = tree.read_text(errors="replace")
        tree_ok = "+--rw interfaces" in content
    return {
        "ok": tree_ok and yang.exists(),
        "pyang_tree_has_interfaces": tree_ok,
        "yang_file_exists": yang.exists(),
        "evidence_sha": sha256_file(tree),
    }


def check_webex() -> dict:
    hash8 = token_hash8()
    room_file = ARTIFACTS / "webex" / "room_create.json"
    msg_file = ARTIFACTS / "webex" / "message_post.json"

    room_title_ok = False
    msg_text_ok = False

    if room_file.exists():
        try:
            data = json.loads(room_file.read_text())
            title = data.get("title", "")
            room_title_ok = hash8 in title
        except Exception:
            pass

    if msg_file.exists():
        try:
            data = json.loads(msg_file.read_text())
            text = data.get("text", "")
            msg_text_ok = hash8 in text
        except Exception:
            pass

    return {
        "ok": room_title_ok and msg_text_ok,
        "room_title_contains_hash8": room_title_ok,
        "message_text_contains_hash8": msg_text_ok,
        "evidence_sha": sha256_file(room_file),
    }


def check_pt() -> dict:
    check_file = ARTIFACTS / "pt" / "external_access_check.json"
    devices_file = ARTIFACTS / "pt" / "network_devices.json"
    hosts_file = ARTIFACTS / "pt" / "hosts.json"
    ticket_file = ARTIFACTS / "pt" / "serviceTicket.txt"

    empty_ticket_seen = False
    devices_ok = False
    hosts_ok = False

    if check_file.exists():
        try:
            text = check_file.read_text(errors="replace")
            empty_ticket_seen = "empty ticket" in text.lower() or "ticket" in text.lower()
        except Exception:
            pass

    if devices_file.exists():
        try:
            data = json.loads(devices_file.read_text())
            # Accept either "version":"1.0" or non-empty response list
            text = devices_file.read_text()
            devices_ok = '"version"' in text or '"response"' in text
        except Exception:
            pass

    if hosts_file.exists():
        try:
            text = hosts_file.read_text()
            hosts_ok = '"version"' in text or '"response"' in text
        except Exception:
            pass

    return {
        "ok": empty_ticket_seen and devices_ok and hosts_ok,
        "empty_ticket_seen": empty_ticket_seen,
        "ticket_saved": ticket_file.exists() and ticket_file.stat().st_size > 0,
        "network_devices_ok": devices_ok,
        "hosts_ok": hosts_ok,
        "evidence_sha": sha256_file(check_file),
    }


def build_summary() -> dict:
    hash8 = token_hash8()
    yang = check_yang()
    webex = check_webex()
    pt = check_pt()

    all_ok = yang["ok"] and webex["ok"] and pt["ok"]

    summary = {
        "schema_version": "5.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "student": {
            "token": get_env("STUDENT_TOKEN"),
            "token_hash8": hash8,
            "name": get_env("STUDENT_NAME", "Baltabaev"),
            "group": get_env("STUDENT_GROUP", ""),
        },
        "yang": yang,
        "webex": webex,
        "pt": pt,
        "validation_passed": all_ok,
    }

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return summary


if __name__ == "__main__":
    print("Building Day 5 summary...")
    summary = build_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nValidation passed: {summary['validation_passed']}")
    print(f"Summary saved to: {SUMMARY_PATH}")
