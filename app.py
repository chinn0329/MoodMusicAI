import streamlit as st
import urllib.parse

# ================== AUTH ==================
from auth.login_ui import render_login_page, render_logout

# ================== UI ==================
from ui.sidebar import render_sidebar
from ui.journal_ui import render_journal_ui
from ui.feedback_ui import render_feedback_ui
from ui.therapy_intake import render_therapy_intake
from ui.explanation import render_ai_explanation

# ================== AI / LOGIC ==================
from ai.model_loader import load_model_and_encoders
from ai.journal_analyzer import analyze_journal_text
from ai.emotion_fusion import fuse_with_journal, get_effective_mood
from ai.predictor import predict_with_personalization

# ================== STORAGE ==================
from storage.journal_store import store_journal_entry, create_session_id

# ================== ANALYTICS ==================
from analytics_ui.dashboard import render_analytics_dashboard
from analytics_ui.journal_trends import render_journal_trends
from analytics_ui.session_comparison import render_session_comparison
from analytics_ui.report_ui import render_report_export

# ================== PERCEPTION ==================
from perception.face_capture import capture_face_image, delete_face_image
from perception.emotion_detector import detect_facial_emotion


# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="MoodMusicAI",
    page_icon="🎵",
    layout="centered"
)


# =================================================
# AUTHENTICATION GATE
# =================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    render_login_page()
    st.stop()

# Authenticated user
user_id = st.session_state.user_id


# =================================================
# SESSION INITIALIZATION
# =================================================
if "session_id" not in st.session_state:
    st.session_state.session_id = create_session_id()

if "therapy_stage" not in st.session_state:
    st.session_state.therapy_stage = "intake"

for key in [
    "history",
    "feedback",
    "detailed_feedback",
    "distress_levels",
    "calm_levels",
    "therapy_insight"
]:
    if key not in st.session_state:
        st.session_state[key] = []


# =================================================
# SESSION RESET FUNCTION
# =================================================
def reset_session():
    from storage.session_store import store_session_summary

    # Store summary BEFORE reset
    if st.session_state.history:
        summary = {
            "dominant_mood": max(
                set(st.session_state.history),
                key=st.session_state.history.count
            ),
            "avg_feedback": (
                st.session_state.feedback.count("Yes") -
                st.session_state.feedback.count("No")
            ) if st.session_state.feedback else 0,
            "avg_distress": (
                sum(st.session_state.distress_levels) /
                len(st.session_state.distress_levels)
            ) if st.session_state.distress_levels else None,
            "avg_calm": (
                sum(st.session_state.calm_levels) /
                len(st.session_state.calm_levels)
            ) if st.session_state.calm_levels else None
        }

        store_session_summary(
            user_id=user_id,
            session_id=st.session_state.session_id,
            summary=summary
        )

    # Reset session state
    st.session_state.session_id = create_session_id()
    st.session_state.therapy_stage = "intake"

    for key in [
        "history", "feedback", "detailed_feedback",
        "distress_levels", "calm_levels",
        "therapy_insight", "therapy_data"
    ]:
        st.session_state.pop(key, None)

    st.rerun()


# =================================================
# HEADER
# =================================================
st.title("🎵 MoodMusicAI")
st.caption("Emotion-aware, therapy-informed music recommendation system")


# =================================================
# SIDEBAR
# =================================================
with st.sidebar:
    render_logout()

    if st.button("🔄 Start New Session"):
        reset_session()

    sidebar_data = render_sidebar()

mode = sidebar_data["mode"]
use_facial_ai = sidebar_data["use_facial_ai"]


# =================================================
# JOURNAL UI
# =================================================
journal_text, journal_saved = render_journal_ui()


# =================================================
# LOAD MODEL
# =================================================
model, mood_encoder, intensity_encoder, goal_encoder = load_model_and_encoders()


# =================================================
# MODE HEADERS
# =================================================
if mode == "Therapy Support Mode":
    st.header("🩺 Therapy Support")
else:
    st.header("🎶 Music Recommendation")


# =================================================
# THERAPY INTAKE PAGE
# =================================================
if mode == "Therapy Support Mode" and st.session_state.therapy_stage == "intake":
    therapy_data = render_therapy_intake()

    if therapy_data["proceed"]:
        st.session_state.therapy_data = therapy_data
        st.session_state.therapy_stage = "recommendation"
        st.rerun()


# =================================================
# INPUT SOURCE RESOLUTION
# =================================================
reported_mood = None
intensity = None
therapy_goal = None
distress_level = None

# ---------- STUDENT MODE ----------
if mode == "Student Mode":
    reported_mood = sidebar_data["reported_mood"]
    intensity = sidebar_data["intensity"]
    therapy_goal = None

# ---------- THERAPY MODE ----------
if mode == "Therapy Support Mode" and "therapy_data" in st.session_state:
    reported_mood = st.session_state.therapy_data["emotional_state"]
    distress_level = st.session_state.therapy_data["stress_level"]
    therapy_goal = st.session_state.therapy_data["desired_outcome"]

    # 🔑 CRITICAL FIX: Map stress (1–10) → intensity classes
    if distress_level <= 3:
        intensity = 1
    elif distress_level <= 7:
        intensity = 2
    else:
        intensity = 3


# =================================================
# RECOMMENDATION TRIGGER
# =================================================
generate = False

if mode == "Student Mode" and st.button("Generate Recommendations"):
    generate = True

if mode == "Therapy Support Mode" and st.session_state.therapy_stage == "recommendation":
    generate = True


# =================================================
# RECOMMENDATION PIPELINE
# =================================================
if generate:

    # -------- Journal Analysis --------
    journal_mood, journal_confidence = None, 0.0
    if journal_text:
        journal_mood, journal_confidence = analyze_journal_text(journal_text)

    # -------- Facial Emotion (Optional) --------
    detected_emotion, emotion_confidence = None, None
    if mode == "Therapy Support Mode" and use_facial_ai:
        img = capture_face_image()
        if img:
            detected_emotion, emotion_confidence = detect_facial_emotion(img)
            delete_face_image(img)

    # -------- Emotion Fusion --------
    intermediate_mood = fuse_with_journal(
        reported_mood,
        journal_mood,
        journal_confidence
    )

    effective_mood = get_effective_mood(
        intermediate_mood,
        detected_emotion,
        emotion_confidence
    )

    # -------- Store Journal --------
    if journal_saved and journal_text:
        store_journal_entry(
            user_id=user_id,
            session_id=st.session_state.session_id,
            journal_text=journal_text,
            inferred_mood=journal_mood,
            confidence=journal_confidence
        )

    # -------- Prediction --------
    (
        prediction,
        base_confidence,
        personalized_confidence,
        adjust_style
    ) = predict_with_personalization(
        model,
        mood_encoder,
        intensity_encoder,
        goal_encoder,
        effective_mood,
        intensity,
        therapy_goal,
        user_id
    )

    # -------- Spotify Query --------
    query = f"{effective_mood} music"
    spotify_url = (
        "https://open.spotify.com/search/"
        + urllib.parse.quote(query)
    )

    # -------- Output --------
    st.success("🎧 Recommendation Ready")
    st.caption(f"AI confidence: {personalized_confidence * 100:.1f}%")
    st.markdown(f"🔗 **[Open on Spotify]({spotify_url})**")

    render_ai_explanation(
        reported_mood=reported_mood,
        effective_mood=effective_mood,
        personalized_confidence=personalized_confidence,
        detected_emotion=detected_emotion,
        emotion_confidence=emotion_confidence,
        user_id=user_id
    )

    st.session_state.history.append(effective_mood)


# =================================================
# FEEDBACK
# =================================================
feedback_submitted, feedback_data, calm_level = render_feedback_ui(mode)

if feedback_submitted and st.session_state.history:
    st.session_state.feedback.append(feedback_data["mood_match"])
    st.session_state.detailed_feedback.append(feedback_data)

    if mode == "Therapy Support Mode" and distress_level is not None:
        st.session_state.distress_levels.append(distress_level)
        st.session_state.calm_levels.append(calm_level)

    st.success("Feedback recorded")


# =================================================
# ANALYTICS
# =================================================
render_journal_trends(user_id)
render_session_comparison(user_id)

render_analytics_dashboard(
    mode=mode,
    mood_history=st.session_state.history,
    feedback_history=st.session_state.feedback,
    detailed_feedback=st.session_state.detailed_feedback,
    distress_levels=st.session_state.distress_levels,
    calm_levels=st.session_state.calm_levels
)

render_report_export(
    mode=mode,
    mood_history=st.session_state.history,
    feedback_history=st.session_state.feedback,
    detailed_feedback=st.session_state.detailed_feedback,
    therapy_insight=st.session_state.therapy_insight
)


# =================================================
# ETHICS FOOTER
# =================================================
st.caption(
    "⚠️ This system is a non-diagnostic prototype. "
    "Therapy mode is supportive in nature and does not replace professional care."
)
