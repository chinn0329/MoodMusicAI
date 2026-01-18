# analytics/report_ui.py

import streamlit as st
from analytics import generate_session_report


def render_report_export(
    mode,
    mood_history,
    feedback_history,
    detailed_feedback,
    therapy_insight
):
    """
    Renders the exportable session report UI.
    """

    with st.expander("📤 Export Session Report"):
        report = generate_session_report(
            mode,
            mood_history,
            feedback_history,
            detailed_feedback,
            therapy_insight
        )

        st.download_button(
            "Download Session Report",
            report,
            "MoodMusicAI_Session_Report.txt",
            mime="text/plain"
        )
