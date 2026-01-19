# ui/sidebar.py

import streamlit as st


def render_sidebar():
    st.title("⚙️ Controls")

    mode = st.selectbox(
        "Select Mode",
        ["Student Mode", "Therapy Support Mode"]
    )

    # Always return mode
    sidebar_data = {
        "mode": mode
    }

    if mode == "Student Mode":
        sidebar_data["reported_mood"] = st.selectbox(
            "Current Mood",
            ["Happy", "Calm", "Sad", "Stressed", "Focused"]
        )

        sidebar_data["intensity"] = st.slider(
            "Intensity",
            1, 10, 5
        )

        sidebar_data["therapy_goal"] = None

    else:
        # Therapy Mode → Sidebar inputs disabled
        sidebar_data["reported_mood"] = None
        sidebar_data["intensity"] = None
        sidebar_data["therapy_goal"] = None

        st.info(
            "Therapy inputs are collected on the next page."
        )

    sidebar_data["use_facial_ai"] = st.checkbox(
        "Enable Facial Emotion Analysis (optional)",
        value=False
    )

    return sidebar_data
