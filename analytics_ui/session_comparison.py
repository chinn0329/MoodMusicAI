# analytics_ui/session_comparison.py

import streamlit as st
import pandas as pd
from storage.session_store import load_sessions


def render_session_comparison(user_id):
    sessions = load_sessions(user_id)
    if len(sessions) < 2:
        return

    df = pd.DataFrame(sessions)

    with st.expander("📊 Session Comparison Analytics"):
        st.dataframe(
            df[[
                "timestamp",
                "dominant_mood",
                "avg_feedback",
                "avg_distress",
                "avg_calm"
            ]]
        )

        if "avg_calm" in df and "avg_distress" in df:
            st.line_chart(
                df[["avg_calm", "avg_distress"]]
            )
