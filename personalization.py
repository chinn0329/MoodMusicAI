import csv
import os

PROFILE_FILE = "user_profiles.csv"


def update_user_profile(user_id, mood, success):
    if not user_id:
        return

    rows = []
    file_exists = os.path.exists(PROFILE_FILE)

    if file_exists:
        with open(PROFILE_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    found = False

    for row in rows:
        if (
            row.get("user_id") == user_id
            and row.get("mood") == mood
        ):
            if success:
                row["success_count"] = str(
                    int(row.get("success_count", 0)) + 1
                )
            else:
                row["failure_count"] = str(
                    int(row.get("failure_count", 0)) + 1
                )
            found = True

    if not found:
        rows.append({
            "user_id": user_id,
            "mood": mood,
            "success_count": "1" if success else "0",
            "failure_count": "0" if success else "1"
        })

    with open(PROFILE_FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["user_id", "mood", "success_count", "failure_count"]
        )
        writer.writeheader()
        writer.writerows(rows)


def get_user_bias(user_id, mood):
    if not user_id or not os.path.exists(PROFILE_FILE):
        return 0.0

    with open(PROFILE_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Defensive access (NO KeyError)
            if (
                row.get("user_id") == user_id
                and row.get("mood") == mood
            ):
                success = int(row.get("success_count", 0))
                failure = int(row.get("failure_count", 0))
                total = success + failure

                if total < 3:
                    return 0.0  # Not enough data

                return (success - failure) / total

    return 0.0
