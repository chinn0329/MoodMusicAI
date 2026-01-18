# auth/login_ui.py

import streamlit as st
from auth.auth_utils import create_user, authenticate_user, user_exists


def render_login_page():
    st.title("🔐 Welcome to MoodMusicAI")

    # Restore login if present
    if "user_id" in st.session_state and user_exists(st.session_state.user_id):
        st.session_state.authenticated = True
        return

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login")

        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input(
            "Password", type="password", key="login_password"
        )

        if st.button("Login"):
            success, message = authenticate_user(
                login_email, login_password
            )
            if success:
                st.session_state.authenticated = True
                st.session_state.user_id = login_email
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    with tab2:
        st.subheader("Sign Up")

        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input(
            "Password", type="password", key="signup_password"
        )

        if st.button("Create Account"):
            success, message = create_user(
                signup_email, signup_password
            )
            if success:
                st.session_state.authenticated = True
                st.session_state.user_id = signup_email
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def render_logout():
    if st.sidebar.button("🚪 Logout"):
        for key in ["authenticated", "user_id", "therapy_stage", "therapy_data"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
