"""
Day 5 — Module 8 Capstone: YANG + Webex + PT-Controller REST API
"""

import os
import json
import hashlib
import requests
from pathlib import Path

# ─── helpers ──────────────────────────────────────────────────────────────────

ARTIFACTS = Path(__file__).parent.parent / "artifacts" / "day5"


def get_token_hash8() -> str:
    token = os.environ.get("STUDENT_TOKEN", "")
    return hashlib.sha256(token.encode()).hexdigest()[:8]


def save_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ saved: {path}")


# ─── Part 2: Webex ────────────────────────────────────────────────────────────

WEBEX_BASE = "https://webexapis.com/v1"


def webex_headers() -> dict:
    token = os.environ.get("WEBEX_TOKEN", "")
    if not token:
        raise ValueError("WEBEX_TOKEN is not set! Export it first.")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def webex_get_me() -> dict:
    """GET /people/me"""
    r = requests.get(f"{WEBEX_BASE}/people/me", headers=webex_headers())
    r.raise_for_status()
    return r.json()


def webex_get_rooms() -> dict:
    """GET /rooms"""
    r = requests.get(f"{WEBEX_BASE}/rooms", headers=webex_headers())
    r.raise_for_status()
    return r.json()


def webex_create_room(title: str) -> dict:
    """POST /rooms"""
    r = requests.post(
        f"{WEBEX_BASE}/rooms",
        headers=webex_headers(),
        json={"title": title},
    )
    r.raise_for_status()
    return r.json()


def webex_post_message(room_id: str, text: str) -> dict:
    """POST /messages"""
    r = requests.post(
        f"{WEBEX_BASE}/messages",
        headers=webex_headers(),
        json={"roomId": room_id, "text": text},
    )
    r.raise_for_status()
    return r.json()


def webex_get_messages(room_id: str) -> dict:
    """GET /messages?roomId=..."""
    r = requests.get(
        f"{WEBEX_BASE}/messages",
        headers=webex_headers(),
        params={"roomId": room_id, "max": 10},
    )
    r.raise_for_status()
    return r.json()


def run_webex() -> None:
    """Run all Webex steps and save evidence."""
    print("\n=== Part 2: Webex ===")
    out = ARTIFACTS / "webex"
    hash8 = get_token_hash8()

    me = webex_get_me()
    save_json(me, out / "me.json")
    print(f"  Logged in as: {me.get('displayName')}")

    rooms = webex_get_rooms()
    save_json(rooms, out / "rooms_list.json")
    print(f"  Rooms count: {len(rooms.get('items', []))}")

    room_title = f"DevNet-Day5-{hash8}"
    room = webex_create_room(room_title)
    save_json(room, out / "room_create.json")
    room_id = room["id"]
    print(f"  Created room: {room_title}")

    msg_text = f"Day5 capstone done! token_hash8={hash8}"
    msg = webex_post_message(room_id, msg_text)
    save_json(msg, out / "message_post.json")
    print(f"  Posted message: {msg_text}")

    msgs = webex_get_messages(room_id)
    save_json(msgs, out / "messages_list.json")
    print(f"  Messages in room: {len(msgs.get('items', []))}")

    print("  ✓ Webex done")


# ─── Part 3: Packet Tracer (стаб для offline) ─────────────────────────────────

PT_BASE = "http://localhost:58000/api/v1"


def pt_check_external_access() -> dict:
    """GET /host without ticket — expects 'empty ticket' response."""
    try:
        r = requests.get(f"{PT_BASE}/host", timeout=3)
        return r.json()
    except Exception as e:
        return {"error": str(e), "note": "PT Controller not reachable (run inside DEVASC VM)"}


def pt_get_service_ticket(username="netadmin", password="Admin_1234!") -> str:
    """POST /ticket to get serviceTicket."""
    r = requests.post(
        f"{PT_BASE}/ticket",
        json={"username": username, "password": password},
        headers={"Content-Type": "application/json"},
    )
    r.raise_for_status()
    data = r.json()
    return data["response"]["serviceTicket"]


def pt_get_network_devices(ticket: str) -> dict:
    """GET /network-device with X-Auth-Token."""
    r = requests.get(
        f"{PT_BASE}/network-device",
        headers={"X-Auth-Token": ticket},
    )
    r.raise_for_status()
    return r.json()


def pt_get_hosts(ticket: str) -> dict:
    """GET /host with X-Auth-Token."""
    r = requests.get(
        f"{PT_BASE}/host",
        headers={"X-Auth-Token": ticket},
    )
    r.raise_for_status()
    return r.json()


def run_pt() -> None:
    """Run PT Controller steps (must be run inside DEVASC VM)."""
    print("\n=== Part 3: Packet Tracer Controller ===")
    out = ARTIFACTS / "pt"

    # Step 1: external access check (no ticket)
    check = pt_check_external_access()
    save_json(check, out / "external_access_check.json")

    # Step 2-4: get ticket and use it
    try:
        ticket = pt_get_service_ticket()
        (out / "serviceTicket.txt").write_text(ticket + "\n")
        print(f"  serviceTicket: {ticket[:20]}...")

        devices = pt_get_network_devices(ticket)
        save_json(devices, out / "network_devices.json")
        print(f"  network-device items: {len(devices.get('response', []))}")

        hosts = pt_get_hosts(ticket)
        save_json(hosts, out / "hosts.json")
        print(f"  host items: {len(hosts.get('response', []))}")

        print("  ✓ PT Controller done")
    except Exception as e:
        print(f"  ⚠ PT error (expected outside VM): {e}")


# ─── main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "webex"

    if mode == "webex":
        run_webex()
    elif mode == "pt":
        run_pt()
    elif mode == "all":
        run_webex()
        run_pt()
    else:
        print("Usage: python day5_module8.py [webex|pt|all]")