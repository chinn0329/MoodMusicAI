# ui/explanation.py

import streamlit as st


def render_ai_explanation(
    reported_mood,
    effective_mood,
    personalized_confidence,
    detected_emotion=None,
    emotion_confidence=None,
    user_id=None
):
    """
    Renders a transparent, human-readable explanation
    of how the AI arrived at the recommendation.
    """

    with st.expander("🧠 How the AI made this decision"):

        st.write(
            f"Your self-reported emotional state was **{reported_mood}**."
        )

        if effective_mood != reported_mood:
            st.write(
                f"Based on additional signals, the system interpreted your "
                f"effective emotional state as **{effective_mood}**."
            )
        else:
            st.write(
                "Your reported emotional state was used directly without modification."
            )

        if detected_emotion:
            st.write(
                f"Facial emotion analysis detected **{detected_emotion}** "
                f"with **{emotion_confidence:.1f}%** confidence."
            )

        st.write(
            f"The machine learning model predicted a "
            f"**{personalized_confidence * 100:.1f}%** likelihood that this "
            "recommendation would match your emotional needs."
        )

        if user_id:
            st.write(
                "Your past interactions were used to personalize this recommendation."
            )

        st.write(
            "The system improves over time through confidence-weighted feedback "
            "and periodic retraining, ensuring safe and explainable learning."
        )
