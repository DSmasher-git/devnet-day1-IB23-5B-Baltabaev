#!/usr/bin/env python3
import os
import json
import hashlib
import argparse
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from faker import Faker

ART = Path("artifacts/day3")
API = os.getenv("LIB_APIHOST", "http://library.demo.local").rstrip("/")
LOGIN = os.getenv("LIB_LOGIN", "cisco")
PASSWORD = os.getenv("LIB_PASSWORD", "Cisco123!")

SCHEMA_VERSION = "3.1"


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def token_hash8(token: str) -> str:
    return sha256(token)[:8]


def save_json(path, data):
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    ART.mkdir(parents=True, exist_ok=True)

    token = os.getenv("STUDENT_TOKEN", "")
    name = os.getenv("STUDENT_NAME", "")
    group = os.getenv("STUDENT_GROUP", "")

    if not token or not name or not group:
        print("ERROR: set STUDENT_TOKEN, STUDENT_NAME, STUDENT_GROUP")
        return 1

    th8 = token_hash8(token)

    if not args.offline:
        s = requests.Session()

        # GET books
        r = s.get(f"{API}/api/v1/books")
        save_json(ART / "books_before.json", {
            "status_code": r.status_code,
            "items": r.json()
        })

        # GET with params
        r2 = s.get(
            f"{API}/api/v1/books",
            params={"includeISBN": "true", "sortBy": "author"}
        )
        save_json(ART / "books_sorted_isbn.json", {
            "status_code": r2.status_code,
            "items": r2.json()
        })

        # LOGIN
        login = s.post(
            f"{API}/api/v1/loginViaBasic",
            auth=(LOGIN, PASSWORD)
        )
        token_api = login.json()["token"]

        # UNIQUE BOOK
        my_book = {
            "id": int(time.time()),
            "title": f"MyBook-{th8}",
            "author": name,
            "isbn": "9780000000000"
        }

        r3 = s.post(
            f"{API}/api/v1/books",
            headers={"X-API-KEY": token_api},
            json=my_book
        )

        save_json(ART / "mybook_post.json", {
            "request": my_book,
            "status_code": r3.status_code
        })

        # ADD 100 BOOKS
        fake = Faker()
        added_ok = 0
        added_fail = 0

        start_id = int(time.time())

        for i in range(start_id, start_id + args.count):
            book = {
                "id": i,
                "title": f"{fake.catch_phrase()} [{th8}]",
                "author": name,
                "isbn": fake.isbn13()
            }

            resp = s.post(
                f"{API}/api/v1/books",
                headers={"X-API-KEY": token_api},
                json=book
            )

            if resp.status_code == 200:
                added_ok += 1
            else:
                added_fail += 1
                print(f"FAIL: id={i} status={resp.status_code}")

        # REPORT (ВАЖНО: правильные поля!)
        save_json(ART / "add100_report.json", {
            "count_requested": args.count,
            "added_ok": added_ok,
            "added_fail": added_fail
        })

        # VERIFY
        r4 = s.get(
            f"{API}/api/v1/books",
            params={
                "author": name,
                "includeISBN": "true",
                "sortBy": "id"
            }
        )

        save_json(ART / "books_by_me.json", {
            "status_code": r4.status_code,
            "items": r4.json()
        })

    # SUMMARY
    summary = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": now(),
        "student": {
            "token": token,
            "token_hash8": th8,
            "name": name,
            "group": group
        }
    }

    save_json(ART / "summary.json", summary)
    print(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())