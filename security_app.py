import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS USER_PLAIN (username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS USER_HASH (username TEXT PRIMARY KEY, password TEXT)')
    conn.commit()
    conn.close()

@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    conn.execute('INSERT INTO USER_PLAIN VALUES (?, ?)', (data['username'], data['password']))
    conn.commit()
    return "Signup V1 Success"

@app.route('/signup/v2', methods=['POST'])
def signup_v2():
    data = request.json
    h = hashlib.sha256(data['password'].encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    conn.execute('INSERT INTO USER_HASH VALUES (?, ?)', (data['username'], h))
    conn.commit()
    return "Signup V2 Success"

# Добавь методы login аналогично (проверка пароля)

if __name__ == "__main__":
    init_db()
    app.run(port=5000)
