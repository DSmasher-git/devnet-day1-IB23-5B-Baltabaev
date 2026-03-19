import requests
import json
import os
import hashlib

# --- Токены ---
WEBEX_TOKEN = os.environ.get("WEBEX_TOKEN", "your_webex_token_here")
STUDENT_TOKEN = os.environ.get("STUDENT_TOKEN", "")

# token_hash8 для уникальности
token_hash8 = hashlib.sha256(STUDENT_TOKEN.encode()).hexdigest()[:8]

BASE_URL = "https://webexapis.com/v1"
headers = {
    "Authorization": f"Bearer {WEBEX_TOKEN}",
    "Content-Type": "application/json"
}

def save(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved: {path}")

# 1. GET /people/me
res = requests.get(f"{BASE_URL}/people/me", headers=headers)
me = res.json()
save(me, "artifacts/day5/webex/me.json")

# 2. GET /rooms
res = requests.get(f"{BASE_URL}/rooms", headers=headers, params={"max": 100})
rooms = res.json()
save(rooms, "artifacts/day5/webex/rooms_list.json")

# 3. POST /rooms — создать комнату с token_hash8 в названии
room_title = f"DevNet Day5 Lab {token_hash8}"
res = requests.post(f"{BASE_URL}/rooms", headers=headers, json={"title": room_title})
room = res.json()
save(room, "artifacts/day5/webex/room_create.json")
room_id = room["id"]
print(f"Room created: {room_title}")

# 4. POST /messages — отправить сообщение с token_hash8
message_text = f"Hello from Day5 lab! hash={token_hash8}"
res = requests.post(f"{BASE_URL}/messages", headers=headers,
                    json={"roomId": room_id, "text": message_text})
msg = res.json()
save(msg, "artifacts/day5/webex/message_post.json")

# 5. GET /messages — прочитать последние сообщения
res = requests.get(f"{BASE_URL}/messages", headers=headers,
                   params={"roomId": room_id, "max": 10})
msgs = res.json()
save(msgs, "artifacts/day5/webex/messages_list.json")

print("All done!")