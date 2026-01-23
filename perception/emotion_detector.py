import requests

FACIAL_API_URL = "https://chinmayi0329-facial-emotion-api.hf.space/analyze-emotion"

def detect_facial_emotion(image_path):
    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                FACIAL_API_URL,
                files=files,
                timeout=10
            )

        if response.status_code != 200:
            return None, None

        data = response.json()
        return data.get("emotion"), data.get("confidence")

    except Exception:
        return None, None
