"""
Tests for Day 5 — Module 8 Capstone
Run with: pytest -q tests/test_day5_module8.py
"""

import json
import hashlib
import os
from pathlib import Path

import pytest
import jsonschema

BASE = Path(__file__).parent.parent
ARTIFACTS = BASE / "artifacts" / "day5"
SCHEMAS = BASE / "schemas"
SUMMARY_PATH = ARTIFACTS / "summary.json"


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def summary():
    assert SUMMARY_PATH.exists(), f"summary.json not found at {SUMMARY_PATH}"
    with open(SUMMARY_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def schema():
    schema_path = SCHEMAS / "day5_summary.schema.json"
    assert schema_path.exists(), "Schema file missing"
    with open(schema_path, encoding="utf-8") as f:
        return json.load(f)


# ─── Schema validation ────────────────────────────────────────────────────────

def test_summary_valid_against_schema(summary, schema):
    """summary.json must validate against day5_summary.schema.json"""
    jsonschema.validate(instance=summary, schema=schema)


def test_schema_version(summary):
    assert summary["schema_version"] == "5.0"


# ─── Student ─────────────────────────────────────────────────────────────────

def test_token_hash8_correct(summary):
    """token_hash8 must equal sha256(STUDENT_TOKEN)[:8]"""
    token = os.environ.get("STUDENT_TOKEN", summary["student"]["token"])
    expected = hashlib.sha256(token.encode()).hexdigest()[:8]
    assert summary["student"]["token_hash8"] == expected


def test_student_name_present(summary):
    assert summary["student"]["name"], "student.name is empty"


# ─── YANG artifacts ───────────────────────────────────────────────────────────

YANG_FILES = [
    "yang/ietf-interfaces.yang",
    "yang/pyang_version.txt",
    "yang/pyang_tree.txt",
]

@pytest.mark.parametrize("rel_path", YANG_FILES)
def test_yang_artifact_exists(rel_path):
    p = ARTIFACTS / rel_path
    assert p.exists(), f"Missing: {p}"
    assert p.stat().st_size > 0, f"Empty file: {p}"


def test_pyang_tree_contains_interfaces():
    tree = ARTIFACTS / "yang" / "pyang_tree.txt"
    assert tree.exists(), "pyang_tree.txt missing"
    content = tree.read_text(errors="replace")
    assert "+--rw interfaces" in content, "pyang tree must contain '+--rw interfaces'"


def test_pyang_tree_contains_enabled():
    tree = ARTIFACTS / "yang" / "pyang_tree.txt"
    if not tree.exists():
        pytest.skip("pyang_tree.txt missing")
    content = tree.read_text(errors="replace")
    assert "enabled" in content, "pyang tree must mention 'enabled'"


def test_yang_summary_ok(summary):
    assert summary["yang"]["yang_file_exists"] is True
    assert summary["yang"]["pyang_tree_has_interfaces"] is True


# ─── Webex artifacts ──────────────────────────────────────────────────────────

WEBEX_FILES = [
    "webex/me.json",
    "webex/rooms_list.json",
    "webex/room_create.json",
    "webex/message_post.json",
    "webex/messages_list.json",
]

@pytest.mark.parametrize("rel_path", WEBEX_FILES)
def test_webex_artifact_exists(rel_path):
    p = ARTIFACTS / rel_path
    assert p.exists(), f"Missing: {p}"
    assert p.stat().st_size > 0, f"Empty file: {p}"


def test_webex_room_title_contains_hash8(summary):
    hash8 = summary["student"]["token_hash8"]
    room_file = ARTIFACTS / "webex" / "room_create.json"
    data = json.loads(room_file.read_text())
    assert hash8 in data.get("title", ""), \
        f"room_create.json title must contain token_hash8={hash8}"


def test_webex_message_contains_hash8(summary):
    hash8 = summary["student"]["token_hash8"]
    msg_file = ARTIFACTS / "webex" / "message_post.json"
    data = json.loads(msg_file.read_text())
    text = data.get("text", "") + data.get("markdown", "")
    assert hash8 in text, \
        f"message_post.json text must contain token_hash8={hash8}"


def test_webex_summary_ok(summary):
    assert summary["webex"]["room_title_contains_hash8"] is True
    assert summary["webex"]["message_text_contains_hash8"] is True


# ─── Packet Tracer artifacts ──────────────────────────────────────────────────

PT_FILES = [
    "pt/external_access_check.json",
    "pt/serviceTicket.txt",
    "pt/network_devices.json",
    "pt/hosts.json",
    "pt/postman_collection.json",
    "pt/postman_environment.json",
    "pt/pt_internal_output.txt",
]

@pytest.mark.parametrize("rel_path", PT_FILES)
def test_pt_artifact_exists(rel_path):
    p = ARTIFACTS / rel_path
    assert p.exists(), f"Missing: {p}"
    assert p.stat().st_size > 0, f"Empty file: {p}"


def test_external_access_check_has_ticket_message():
    f = ARTIFACTS / "pt" / "external_access_check.json"
    content = f.read_text(errors="replace").lower()
    assert "ticket" in content, \
        "external_access_check.json must contain word 'ticket'"


def test_service_ticket_not_empty():
    f = ARTIFACTS / "pt" / "serviceTicket.txt"
    ticket = f.read_text().strip()
    assert len(ticket) > 10, "serviceTicket.txt seems too short"


def test_pt_summary_ok(summary):
    assert summary["pt"]["empty_ticket_seen"] is True
    assert summary["pt"]["ticket_saved"] is True


# ─── validation_passed ────────────────────────────────────────────────────────

def test_validation_passed(summary):
    assert summary["validation_passed"] is True, \
        "summary.json validation_passed must be True — check yang/webex/pt sections"