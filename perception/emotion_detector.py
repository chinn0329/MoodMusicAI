from deepface import DeepFace

def detect_facial_emotion(image_path):
    try:
        result = DeepFace.analyze(
            img_path=image_path,
            actions=["emotion"],
            enforce_detection=False
        )

        dominant_emotion = result[0]["dominant_emotion"]
        confidence = result[0]["emotion"][dominant_emotion]

        return dominant_emotion, confidence

    except Exception as e:
        return None, None
