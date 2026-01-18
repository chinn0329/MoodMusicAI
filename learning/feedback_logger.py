# learning/feedback_logger.py

import csv
import os

FEEDBACK_FILE = "data/user_feedback_data.csv"


def log_user_feedback(mood, intensity, goal, feedback, confidence):
    """
    Confidence-weighted feedback logging for self-learning.
    """

    if feedback not in ["Yes", "Partially", "No"]:
        return

    label = 0 if feedback == "No" else 1
    goal_value = goal if goal else "None"

    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(FEEDBACK_FILE)

    with open(FEEDBACK_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                ["mood", "intensity", "goal", "match", "confidence"]
            )

        writer.writerow([
            mood,
            intensity,
            goal_value,
            label,
            round(float(confidence), 3)
        ])
