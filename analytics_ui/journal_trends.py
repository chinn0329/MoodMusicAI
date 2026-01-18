# analytics_ui/journal_trends.py

import streamlit as st
import pandas as pd
from storage.journal_store import get_user_journals


MOOD_SCORE_MAP = {
    "Happy": 1,
    "Calm": 0,
    "Sad": -1,
    "Stressed": -2
}


def render_journal_trends(user_id):
    """
    Visualizes emotional trends from journal entries.
    """

    journals = get_user_journals(user_id)

    if not journals:
        return

    df = pd.DataFrame(journals)

    if "inferred_mood" not in df or df.empty:
        return

    df["mood_score"] = df["inferred_mood"].map(MOOD_SCORE_MAP)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.dropna(subset=["mood_score"])

    if df.empty:
        return

    with st.expander("📈 Journal Mood Trends"):
        st.line_chart(
            df.sort_values("timestamp")[["timestamp", "mood_score"]]
            .set_index("timestamp")
        )

        st.caption(
            "Trend shows emotional tone inferred from journal entries over time. "
            "Positive values indicate uplifting emotions; negative values indicate distress."
        )
