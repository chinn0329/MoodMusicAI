# perception/emotion_detector.py

def detect_facial_emotion(image_path):
    """
    Attempts to detect facial emotion.
    Falls back gracefully if DeepFace is unavailable.
    """

    try:
        from deepface import DeepFace
    except ImportError:
        # DeepFace not available (e.g., Streamlit Cloud)
        return None, None

    try:
        result = DeepFace.analyze(
            img_path=image_path,
            actions=["emotion"],
            enforce_detection=False
        )

        dominant_emotion = result[0]["dominant_emotion"]
        confidence = max(result[0]["emotion"].values())

        return dominant_emotion, confidence

    except Exception:
        return None, None
