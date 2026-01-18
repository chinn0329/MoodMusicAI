# ai/predictor.py

import numpy as np
from personalization import get_user_bias


def predict_with_personalization(
    model,
    mood_encoder,
    intensity_encoder,
    goal_encoder,
    effective_mood,
    intensity,
    therapy_goal,
    user_id
):
    """
    Runs ML prediction and applies per-user personalization.

    Returns:
    - prediction (0/1)
    - base_confidence
    - personalized_confidence
    - adjust_style (bool)
    """

    goal_value = therapy_goal if therapy_goal else "None"

    X_input = np.array([[
        mood_encoder.transform([effective_mood])[0],
        intensity_encoder.transform([intensity])[0],
        goal_encoder.transform([goal_value])[0]
    ]])

    prediction = model.predict(X_input)[0]
    base_confidence = model.predict_proba(X_input)[0][1]

    # Personalization bias
    user_bias = get_user_bias(user_id, effective_mood)
    personalized_confidence = base_confidence + (0.1 * user_bias)
    personalized_confidence = min(max(personalized_confidence, 0), 1)

    adjust_style = personalized_confidence < 0.5

    return (
        prediction,
        base_confidence,
        personalized_confidence,
        adjust_style
    )
