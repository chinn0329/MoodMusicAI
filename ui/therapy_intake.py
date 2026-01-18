# ui/therapy_intake.py

import streamlit as st


def render_therapy_intake():
    """
    Collects detailed therapeutic inputs.
    Returns a dictionary of responses.
    """

    st.subheader("🩺 Therapeutic Intake")

    emotional_state = st.selectbox(
        "How would you describe your emotional state right now?",
        ["Calm", "Anxious", "Low", "Overwhelmed", "Numb", "Irritable"]
    )

    stress_level = st.slider(
        "Current stress level",
        1, 10, 5
    )

    primary_trigger = st.selectbox(
        "What is the primary source of distress?",
        [
            "Academic / Work pressure",
            "Relationships",
            "Health concerns",
            "Uncertainty about future",
            "Self-esteem",
            "No specific trigger"
        ]
    )

    coping_capacity = st.radio(
        "How well do you feel you are coping right now?",
        ["Managing well", "Some difficulty", "Struggling"]
    )

    physical_symptoms = st.selectbox(
    "Are you experiencing any physical symptoms right now?",
    [
        "None",
        "Restlessness or racing heart",
        "Fatigue or low energy",
        "Muscle tension",
        "Difficulty breathing"
    ]
)

    duration = st.selectbox(
        "How long have you been feeling this way?",
        [
            "Just today",
            "A few days",
            "A few weeks",
            "Longer than a month"
        ]
    )

    desired_outcome = st.selectbox(
        "What would you like music to help with right now?",
        [
            "Calming anxiety",
            "Grounding emotions",
            "Improving focus",
            "Helping with sleep",
            "Emotional release"
        ]
    )

    proceed = st.button("Continue to Recommendations")

    return {
    "emotional_state": emotional_state,
    "stress_level": stress_level,
    "primary_trigger": primary_trigger,
    "coping_capacity": coping_capacity,
    "physical_symptoms": physical_symptoms,
    "duration": duration,
    "desired_outcome": desired_outcome,
    "proceed": proceed
}
