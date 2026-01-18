import streamlit as st
import urllib.parse

# -------------------- UI MODULES --------------------
from ui.sidebar import render_sidebar
from ui.explanation import render_ai_explanation
from ui.feedback_ui import render_feedback_ui
from ui.journal_ui import render_journal_ui
from ui.therapy_intake import render_therapy_intake

# -------------------- AI MODULES --------------------
from ai.model_loader import load_model_and_encoders
from ai.emotion_fusion import get_effective_mood, fuse_with_journal
from ai.predictor import predict_with_personalization
from ai.journal_analyzer import analyze_journal_text

# -------------------- LEARNING & PERSONALIZATION --------------------
from learning.feedback_logger import log_user_feedback
from personalization import update_user_profile

# -------------------- PERCEPTION --------------------
from perception.face_capture import capture_face_image, delete_face_image
from perception.emotion_detector import detect_facial_emotion

# -------------------- ANALYTICS & REPORTS --------------------
from analytics_ui.dashboard import render_analytics_dashboard
from analytics_ui.report_ui import render_report_export
from analytics_ui.journal_trends import render_journal_trends

# -------------------- JOURNAL STORAGE --------------------
from storage.journal_store import store_journal_entry, create_session_id

# -------------------- MUSIC RECOMMENDER --------------------
from recommender import (
    get_music_query,
    explain_recommendation,
    therapy_goal_modifier
)
# -------------------- USER LOGIN --------------------
from auth.login_ui import render_login_page
from auth.login_ui import render_login_page, render_logout

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="MoodMusicAI",
    page_icon="🎧",
    layout="centered"
)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    render_login_page()
    st.stop()

st.title("🎵 MoodMusicAI")
st.caption(
    "Explainable, self-learning AI system for mood-based music & therapy support"
)

# -------------------------------------------------
# Session Initialization
# -------------------------------------------------
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

# -------------------------------------------------
# Journal UI (Top Right Button)
# -------------------------------------------------
journal_text, journal_saved = render_journal_ui()

# -------------------------------------------------
# Load AI Model & Encoders
# -------------------------------------------------
model, mood_encoder, intensity_encoder, goal_encoder = load_model_and_encoders()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    render_logout()
    sidebar_data = render_sidebar()


user_id = sidebar_data["user_id"]
mode = sidebar_data["mode"]
reported_mood = sidebar_data["reported_mood"]
intensity = sidebar_data["intensity"]
therapy_goal = sidebar_data["therapy_goal"]
distress_level = sidebar_data["distress_level"]
use_facial_ai = sidebar_data["use_facial_ai"]

# -------------------------------------------------
# Recommendation Section
# -------------------------------------------------
if mode == "Therapy Support Mode":
    st.header("🩺 Therapy Support")
else:
    st.header("🎶 Music Recommendation")

# -------------------------------------------------
# Therapy Intake Flow (ONLY for Therapy Mode)
# -------------------------------------------------
if mode == "Therapy Support Mode" and st.session_state.therapy_stage == "intake":

    therapy_data = render_therapy_intake()

    if therapy_data["proceed"]:
        st.session_state.therapy_data = therapy_data
        st.session_state.therapy_stage = "recommendation"
        st.rerun()


if (
    (mode == "Student Mode" and st.button("Generate Recommendations")) or
    (mode == "Therapy Support Mode" and st.session_state.therapy_stage == "recommendation")
):

    # -------- Journal Analysis --------
    journal_mood = None
    journal_confidence = 0.0

    if journal_text:
        journal_mood, journal_confidence = analyze_journal_text(journal_text)

    # -------- Facial Emotion Detection --------
    detected_emotion = None
    emotion_confidence = None

    if mode == "Therapy Support Mode" and use_facial_ai:
        image_path = capture_face_image()
        if image_path:
            detected_emotion, emotion_confidence = detect_facial_emotion(image_path)
            delete_face_image(image_path)

    # -------- Emotion Fusion Pipeline --------
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

    # -------- Store Journal Securely --------
    if journal_saved and journal_text:
        store_journal_entry(
            user_id=user_id,
            session_id=st.session_state.session_id,
            journal_text=journal_text,
            inferred_mood=journal_mood,
            confidence=journal_confidence
        )

    # -------- AI Prediction + Personalization --------
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

    # -------- Map Therapy Intake to Therapy Goal --------
    if mode == "Therapy Support Mode" and "therapy_data" in st.session_state:

        desired_outcome = st.session_state.therapy_data["desired_outcome"]

        therapy_goal_map = {
            "Calming anxiety": "Stress Reduction",
            "Grounding emotions": "Emotional Grounding",
            "Improving focus": "Focus Enhancement",
            "Helping with sleep": "Sleep Preparation",
            "Emotional release": "Emotional Processing"
        }

        therapy_goal = therapy_goal_map.get(desired_outcome, therapy_goal)

    # -------- Music Query --------
    query = get_music_query(effective_mood, intensity, adjust_style)

    if mode == "Therapy Support Mode" and therapy_goal:
        query += " " + therapy_goal_modifier(therapy_goal)

    spotify_url = (
        "https://open.spotify.com/search/"
        + urllib.parse.quote(query)
    )

    explanation = explain_recommendation(
        effective_mood,
        intensity,
        mode
    )

    st.session_state.history.append(effective_mood)

    # -------- Output --------
    st.success("🎧 Recommendation Ready")
    st.info(explanation)

    st.caption(
        f"🤖 AI Confidence: {personalized_confidence * 100:.1f}% likelihood of emotional match"
    )

    if journal_mood:
        st.caption(
            f"📝 Journal analysis suggested **{journal_mood}** "
            f"(confidence {journal_confidence:.2f})"
        )

    if detected_emotion:
        st.caption(
            f"📷 Facial emotion detected **{detected_emotion}** "
            f"({emotion_confidence:.1f}% confidence)"
        )

    st.markdown(f"🔗 **[Open music on Spotify]({spotify_url})**")

    # -------- Explainable AI --------
    render_ai_explanation(
        reported_mood=reported_mood,
        effective_mood=effective_mood,
        personalized_confidence=personalized_confidence,
        detected_emotion=detected_emotion,
        emotion_confidence=emotion_confidence,
        user_id=user_id
    )

# -------------------------------------------------
# Feedback Section
# -------------------------------------------------
feedback_submitted, feedback_data, calm_level = render_feedback_ui(mode)

if feedback_submitted and st.session_state.history:

    st.session_state.detailed_feedback.append(feedback_data)
    st.session_state.feedback.append(feedback_data["mood_match"])

    log_user_feedback(
        mood=st.session_state.history[-1],
        intensity=intensity,
        goal=therapy_goal,
        feedback=feedback_data["mood_match"],
        confidence=personalized_confidence
    )

    update_user_profile(
        user_id=user_id,
        mood=st.session_state.history[-1],
        success=feedback_data["mood_match"] != "No"
    )

    if mode == "Therapy Support Mode" and calm_level is not None:
        st.session_state.distress_levels.append(distress_level)
        st.session_state.calm_levels.append(calm_level)

    st.success("Feedback recorded. Learning updated.")

# -------------------------------------------------
# Analytics & Reports
# -------------------------------------------------
render_journal_trends(user_id)

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

# -------------------------------------------------
# Ethics Footer
# -------------------------------------------------
st.caption(
    "⚠️ Ethical Notice: Journal entries and facial emotion analysis are optional, "
    "processed locally, and stored per user and per session. "
    "This system is a non-diagnostic prototype and does not replace professional care."
)
