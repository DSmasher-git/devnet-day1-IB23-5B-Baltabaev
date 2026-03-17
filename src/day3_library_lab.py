#!/usr/bin/env python3
import os
import json
import hashlib
import argparse
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
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


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
        r2 = s.get(f"{API}/api/v1/books",
                   params={"includeISBN": "true", "sortBy": "author"})
        save_json(ART / "books_sorted_isbn.json", {
            "status_code": r2.status_code,
            "items": r2.json()
        })

        # Login
        login = s.post(f"{API}/api/v1/loginViaBasic",
                       auth=(LOGIN, PASSWORD))
        token_api = login.json()["token"]

        # Add unique book
        my_book = {
            "id": 9000,
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

        # Add 100 books
        fake = Faker()
        added = 0

        for i in range(args.count):
            book = {
                "id": 10000 + i,
                "title": fake.catch_phrase(),
                "author": name,
                "isbn": fake.isbn13()
            }

            resp = s.post(
                f"{API}/api/v1/books",
                headers={"X-API-KEY": token_api},
                json=book
            )

            if resp.status_code == 200:
                added += 1

        save_json(ART / "add100_report.json", {
            "requested": args.count,
            "added": added
        })

        # Books by author
        r4 = s.get(f"{API}/api/v1/books",
                   params={"author": name,
                           "includeISBN": "true",
                           "sortBy": "id"})

        save_json(ART / "books_by_me.json", {
            "status_code": r4.status_code,
            "items": r4.json()
        })

    # Summary
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