import json
import os
import hashlib

USERS_FILE = "users.json"

def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register(username, password):
    if not username or not password:
        return False, "Username and password required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    users = load_users()
    if username.lower() in users:
        return False, "Username already taken."
    users[username.lower()] = _hash(password)
    save_users(users)
    return True, f"Account created for {username}!"

def login(username, password):
    users = load_users()
    hashed = users.get(username.lower())
    return hashed == _hash(password)