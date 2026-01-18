# storage/journal_store.py

import json
import os
import uuid
from datetime import datetime

JOURNAL_DIR = "data/journals"


def _get_user_journal_file(user_id):
    os.makedirs(JOURNAL_DIR, exist_ok=True)
    safe_user = user_id if user_id else "anonymous"
    return os.path.join(JOURNAL_DIR, f"{safe_user}_journals.json")


def create_session_id():
    return str(uuid.uuid4())


def store_journal_entry(
    user_id,
    session_id,
    journal_text,
    inferred_mood=None,
    confidence=0.0
):
    """
    Stores journal securely per user and per session.
    """

    journal_file = _get_user_journal_file(user_id)

    entry = {
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat(),
        "journal_text": journal_text,
        "inferred_mood": inferred_mood,
        "confidence": round(float(confidence), 3)
    }

    if os.path.exists(journal_file):
        with open(journal_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(journal_file, "w") as f:
        json.dump(data, f, indent=2)

def get_user_journals(user_id):
    """
    Returns all stored journal entries for a user.
    """
    journal_file = _get_user_journal_file(user_id)

    if not os.path.exists(journal_file):
        return []

    with open(journal_file, "r") as f:
        return json.load(f)
