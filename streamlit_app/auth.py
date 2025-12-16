import streamlit as st
from api import register_user, login


def auth_page():
    st.title("🔐 Authentication")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            r = login(username, password)
            if r.status_code == 200:
                st.session_state.token = r.json()["access_token"]
                st.success("Logged in successfully")
            else:
                st.error(r.text)

    with tab2:
        st.subheader("Register")
        username = st.text_input("New Username")
        email = st.text_input("Email")
        password = st.text_input("New Password", type="password")
        role = st.selectbox("Role", ["user", "admin"])

        if st.button("Register"):
            r = register_user(
                {
                    "username": username,
                    "email": email,
                    "password": password,
                    "role": role,
                }
            )
            if r.status_code == 201:
                st.success("Registered successfully")
            else:
                st.error(r.text)
