# ai/journal_analyzer.py

def analyze_journal_text(journal_text):
    """
    Lightweight, explainable emotion extraction from journal text.
    No external libraries required.
    """

    if not journal_text:
        return None, 0.0

    text = journal_text.lower()

    positive_words = ["happy", "calm", "relaxed", "peace", "hope", "joy"]
    negative_words = ["sad", "anxious", "stress", "angry", "tired", "upset", "worried"]

    pos_score = sum(word in text for word in positive_words)
    neg_score = sum(word in text for word in negative_words)

    if pos_score > neg_score:
        return "Happy", min(1.0, pos_score / 3)
    elif neg_score > pos_score:
        return "Sad", min(1.0, neg_score / 3)
    else:
        return "Calm", 0.3
