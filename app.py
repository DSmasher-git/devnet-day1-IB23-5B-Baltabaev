from flask import Flask
import os
import hashlib

app = Flask(__name__)

def token_hash8():
    token = os.getenv("STUDENT_TOKEN", "")
    return hashlib.sha256(token.encode()).hexdigest()[:8]

@app.route("/")
def home():
    return f"Hello! TOKEN_HASH8={token_hash8()}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=False)