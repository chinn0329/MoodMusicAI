# ui/journal_ui.py

import streamlit as st


def render_journal_ui():
    """
    Renders a journal entry section triggered by a top-right button.
    Returns:
    - journal_text (str or None)
    - journal_saved (bool)
    """

    journal_text = None
    journal_saved = False

    col1, col2 = st.columns([5, 1])
    with col2:
        open_journal = st.button("📝 Journal")

    if open_journal:
        st.markdown("### 🧠 Personal Journal Entry")

        journal_text = st.text_area(
            "Write freely about how you're feeling right now",
            height=200,
            placeholder="Thoughts, emotions, worries, reflections..."
        )

        if st.button("Save Journal Entry"):
            if journal_text and journal_text.strip():
                journal_saved = True
                st.success("Journal entry saved for this session.")

    return journal_text, journal_saved
