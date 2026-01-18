import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import joblib
import os
import numpy as np

BASE_DATA = "training_data.csv"
USER_DATA = "user_feedback_data.csv"

# -----------------------------
# Load base data
# -----------------------------
base_data = pd.read_csv(BASE_DATA)
base_data["goal"] = base_data["goal"].fillna("None")

# Base data gets neutral weight
base_data["weight"] = 1.0

data = base_data.copy()

# -----------------------------
# Append user feedback
# -----------------------------
if os.path.exists(USER_DATA):
    try:
        user_data = pd.read_csv(USER_DATA)

        if not user_data.empty and "match" in user_data.columns:
            user_data["goal"] = user_data["goal"].fillna("None")

            # Confidence-weighted samples
            user_data["weight"] = user_data["confidence"].clip(0.2, 1.0)

            data = pd.concat([data, user_data], ignore_index=True)

    except Exception:
        print("User feedback data invalid. Skipping.")

# -----------------------------
# Ensure class diversity
# -----------------------------
if data["match"].nunique() < 2:
    print(
        "Not enough class diversity for retraining.\n"
        "Need both positive and negative feedback."
    )
    exit()

# -----------------------------
# Encode features
# -----------------------------
mood_enc = LabelEncoder()
intensity_enc = LabelEncoder()
goal_enc = LabelEncoder()

data["mood_enc"] = mood_enc.fit_transform(data["mood"])
data["intensity_enc"] = intensity_enc.fit_transform(data["intensity"])
data["goal_enc"] = goal_enc.fit_transform(data["goal"])

X = data[["mood_enc", "intensity_enc", "goal_enc"]]
y = data["match"]
weights = data["weight"]

# -----------------------------
# Train weighted model
# -----------------------------
model = LogisticRegression(max_iter=1000)
model.fit(X, y, sample_weight=weights)

# -----------------------------
# Save updated model
# -----------------------------
joblib.dump(model, "mood_model.pkl")
joblib.dump(mood_enc, "mood_encoder.pkl")
joblib.dump(intensity_enc, "intensity_encoder.pkl")
joblib.dump(goal_enc, "goal_encoder.pkl")

print("✅ Model retrained using confidence-weighted learning.")
