# ui/feedback_ui.py

import streamlit as st


def render_feedback_ui(mode):
    """
    Renders feedback UI and returns feedback data when submitted.

    Returns:
    - feedback_submitted (bool)
    - feedback_data (dict or None)
    - calm_level (int or None)
    """

    feedback_data = {}
    calm_level = None
    feedback_submitted = False

    with st.expander("📝 Feedback"):

        feedback_data["mood_match"] = st.radio(
            "Did the music match your emotional state?",
            ["Yes", "Partially", "No"]
        )

        feedback_data["emotional_shift"] = st.selectbox(
            "Emotional change after listening",
            ["More calm", "Slightly improved", "No change", "More tense"]
        )

        feedback_data["coping_effectiveness"] = st.slider(
            "Coping effectiveness",
            1, 5, 3
        )

        feedback_data["comfort_level"] = st.slider(
            "Comfort level",
            1, 5, 3
        )

        if mode == "Therapy Support Mode":
            calm_level = st.slider(
                "Calmness after listening",
                1, 5, 3
            )

        feedback_submitted = st.button("Submit Feedback")

    return feedback_submitted, feedback_data, calm_level
