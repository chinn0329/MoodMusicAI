import streamlit as st

def render_sidebar():
    st.header("🎛 Controls")

    user_id = st.text_input(
        "User ID (optional)",
        help="Any nickname. Used only for personalization."
    )

    mode = st.radio(
        "Usage Mode",
        ["Student Mode", "Therapy Support Mode"]
    )

    if mode == "Therapy Support Mode":
        reported_mood = st.selectbox(
            "Current Emotional State (self-reported)",
            ["Happy", "Sad", "Stressed", "Calm", "Focused"],
            help="How you are feeling right now. This is the primary emotional input."
        )
    else:
        reported_mood = st.selectbox(
            "Mood",
            ["Happy", "Sad", "Stressed", "Calm", "Focused"]
        )

    intensity = st.radio(
        "Mood Intensity",
        ["Low", "Medium", "High"]
    )

    therapy_goal = None
    distress_level = None
    use_facial_ai = False

    if mode == "Therapy Support Mode":
        st.divider()
        st.subheader("🩺 Therapy Inputs")

        therapy_goal = st.selectbox(
            "Therapeutic Goal",
            [
                "Stress Reduction",
                "Emotional Grounding",
                "Anxiety Calming",
                "Sleep Preparation"
            ]
        )

        distress_level = st.slider(
            "Emotional Distress Level",
            1, 5, 3
        )

        use_facial_ai = st.checkbox(
            "Allow facial emotion detection (webcam)",
            help="Optional. Used only to refine mood when confidence is high."
        )

    return {
        "user_id": user_id,
        "mode": mode,
        "reported_mood": reported_mood,
        "intensity": intensity,
        "therapy_goal": therapy_goal,
        "distress_level": distress_level,
        "use_facial_ai": use_facial_ai
    }
