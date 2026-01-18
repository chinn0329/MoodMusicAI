# analytics_ui/dashboard.py

import streamlit as st


def render_analytics_dashboard(
    mode,
    mood_history,
    feedback_history,
    detailed_feedback,
    distress_levels,
    calm_levels
):
    """
    Renders analytics for both Student and Therapy modes.
    """

    st.subheader("📊 Session Analytics")

    if not mood_history:
        st.info("No session data available yet.")
        return

    # ---------------- Mood Distribution ----------------
    st.markdown("### Mood Distribution")
    st.bar_chart(
        {m: mood_history.count(m) for m in set(mood_history)}
    )

    # ---------------- Feedback Summary ----------------
    if feedback_history:
        st.markdown("### Feedback Summary")
        feedback_counts = {
            "Yes": feedback_history.count("Yes"),
            "Partially": feedback_history.count("Partially"),
            "No": feedback_history.count("No")
        }
        st.bar_chart(feedback_counts)

    # ---------------- Therapy Insights ----------------
    if mode == "Therapy Support Mode" and distress_levels and calm_levels:
        st.markdown("### 🧠 Therapeutic Insight")

        avg_distress = sum(distress_levels) / len(distress_levels)
        avg_calm = sum(calm_levels) / len(calm_levels)

        if avg_calm > avg_distress:
            insight = "Overall calming effect observed during the session."
        else:
            insight = "User may benefit from extended calming or grounding support."

        st.success(insight)
        st.session_state.therapy_insight = insight
