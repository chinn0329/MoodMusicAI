# ai/emotion_fusion.py

FACIAL_TO_MOOD_MAP = {
    "happy": "Happy",
    "sad": "Sad",
    "neutral": "Calm",
    "angry": "Stressed",
    "fear": "Stressed",
    "surprise": "Happy",
    "disgust": "Stressed"
}


def fuse_with_journal(
    reported_mood,
    journal_mood=None,
    journal_confidence=0.0,
    threshold=0.4
):
    """
    Journal acts as a soft emotional bias, not a hard override.
    """

    if not journal_mood or journal_confidence < threshold:
        return reported_mood

    if journal_mood == reported_mood:
        return reported_mood

    if reported_mood in ["Happy", "Focused"] and journal_mood in ["Sad", "Stressed"]:
        return "Calm"

    return reported_mood


def get_effective_mood(
    base_mood,
    detected_emotion=None,
    emotion_confidence=None,
    confidence_threshold=70
):
    """
    Facial emotion refinement (confidence-gated).
    """

    if (
        detected_emotion
        and emotion_confidence is not None
        and emotion_confidence >= confidence_threshold
    ):
        return FACIAL_TO_MOOD_MAP.get(detected_emotion.lower(), base_mood)

    return base_mood
