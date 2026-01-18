# auth/auth_utils.py

import json
import os
import hashlib
from datetime import datetime

USERS_FILE = "data/users.json"


def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(email, password):
    users = _load_users()

    if email in users:
        return False, "User already exists"

    users[email] = {
        "password_hash": hash_password(password),
        "created_at": datetime.utcnow().isoformat()
    }

    _save_users(users)
    return True, "Account created successfully"


def authenticate_user(email, password):
    users = _load_users()

    if email not in users:
        return False, "User does not exist"

    if users[email]["password_hash"] != hash_password(password):
        return False, "Incorrect password"

    return True, "Login successful"

def user_exists(email):
    users = _load_users()
    return email in users
