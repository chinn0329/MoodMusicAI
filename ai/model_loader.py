# ai/model_loader.py

import joblib


def load_model_and_encoders():
    """
    Loads the trained ML model and encoders.
    Centralizing this avoids duplication and makes upgrades easy.
    """

    model = joblib.load("mood_model.pkl")
    mood_encoder = joblib.load("mood_encoder.pkl")
    intensity_encoder = joblib.load("intensity_encoder.pkl")
    goal_encoder = joblib.load("goal_encoder.pkl")

    return model, mood_encoder, intensity_encoder, goal_encoder
