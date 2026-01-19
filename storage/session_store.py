# storage/session_store.py

import json
import os
from datetime import datetime

SESSION_DIR = "data/sessions"


def store_session_summary(user_id, session_id, summary):
    os.makedirs(SESSION_DIR, exist_ok=True)
    file_path = os.path.join(SESSION_DIR, f"{user_id}_sessions.json")

    entry = {
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat(),
        **summary
    }

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def load_sessions(user_id):
    file_path = os.path.join(SESSION_DIR, f"{user_id}_sessions.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)
