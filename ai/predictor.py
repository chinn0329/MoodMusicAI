# ai/predictor.py

import numpy as np


# -------------------------------------------------
# SAFE ENCODERS
# -------------------------------------------------

def safe_encode_intensity(intensity, intensity_encoder):
    """
    Safely encodes numeric or unknown intensity values.
    """
    known_classes = list(intensity_encoder.classes_)

    # Numeric encoder
    if isinstance(known_classes[0], (int, float, np.integer, np.floating)):
        if intensity in known_classes:
            return intensity_encoder.transform([intensity])[0]
        closest = min(known_classes, key=lambda x: abs(x - intensity))
        return intensity_encoder.transform([closest])[0]

    # Categorical encoder
    if intensity <= 3:
        mapped = known_classes[0]
    elif intensity <= 7:
        mapped = known_classes[len(known_classes) // 2]
    else:
        mapped = known_classes[-1]

    return intensity_encoder.transform([mapped])[0]


def safe_encode_goal(goal, goal_encoder):
    """
    Safely encodes therapy goals, even if unseen.
    """
    known_classes = list(goal_encoder.classes_)

    if goal in known_classes:
        return goal_encoder.transform([goal])[0]

    # Semantic fallback mapping
    goal_lower = goal.lower()

    if "anxiety" in goal_lower or "stress" in goal_lower:
        mapped = known_classes[0]
    elif "focus" in goal_lower or "clarity" in goal_lower:
        mapped = known_classes[len(known_classes) // 2]
    elif "sleep" in goal_lower or "relax" in goal_lower:
        mapped = known_classes[-1]
    else:
        mapped = known_classes[0]  # safest fallback

    return goal_encoder.transform([mapped])[0]


# -------------------------------------------------
# PREDICTION FUNCTION
# -------------------------------------------------

def predict_with_personalization(
    model,
    mood_encoder,
    intensity_encoder,
    goal_encoder,
    mood,
    intensity,
    therapy_goal,
    user_id
):
    """
    Generates emotion-aware music recommendations safely.
    """

    # Encode mood (mood labels are controlled)
    mood_encoded = mood_encoder.transform([mood])[0]

    # Encode intensity safely
    intensity_encoded = safe_encode_intensity(
        intensity,
        intensity_encoder
    )

    # Encode therapy goal safely
    if therapy_goal:
        goal_encoded = safe_encode_goal(
            therapy_goal,
            goal_encoder
        )
    else:
        goal_encoded = 0  # neutral goal

    # Build feature vector
    features = np.array(
        [[mood_encoded, intensity_encoded, goal_encoded]]
    )

    # Model prediction
    prediction = model.predict(features)[0]

    # Confidence estimation
    if hasattr(model, "predict_proba"):
        base_confidence = max(model.predict_proba(features)[0])
    else:
        base_confidence = 0.7

    # Personalization placeholder
    personalized_confidence = min(base_confidence + 0.05, 1.0)
    adjust_style = "balanced"

    return (
        prediction,
        base_confidence,
        personalized_confidence,
        adjust_style
    )
