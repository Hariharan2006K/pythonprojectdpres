import streamlit as st
from database import create_user, validate_login

st.set_page_config(page_title="DPRES", page_icon="⛑️", layout="wide")

# Auth State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None

pages = {
    "Navigation": [
        st.Page("views/home.py", title="Basecamp", icon="📍"),
        st.Page("views/learning.py", title="Survival Guides", icon="🎒"),
        st.Page("views/mapping.py", title="Interactive Mapping", icon="🗺️"),
        st.Page("views/gobag.py", title="Go-Bag Builder", icon="🧳"),
        st.Page("views/directory.py", title="SOS Directory", icon="📇"),
        st.Page("views/quiz.py", title="Knowledge Assessment", icon="📝"),
        st.Page("views/dashboard.py", title="Readiness Metrics", icon="📋"),
    ]
}

pg = st.navigation(pages)

with st.sidebar:
    st.markdown("---")
    if not st.session_state.logged_in:
        st.subheader("Operator Login")
        auth_mode = st.radio("Select Action:", ["Login", "Register"], label_visibility="collapsed")
        with st.form("auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                if auth_mode == "Register":
                    if create_user(username, password):
                        st.success("Registration successful! Please log in.")
                    else:
                        st.error("Username already taken. Try another.")
                else:
                    user_id = validate_login(username, password)
                    if user_id:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
    else:
        st.success(f"Authenticated as: **{st.session_state.username}**")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
            
    st.markdown("---")
    st.caption("Disaster Preparedness & Response Protocol")

pg.run()
