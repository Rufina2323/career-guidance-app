import streamlit as st
from api import *
from auth import auth_page
from forms import ml_input_form

st.set_page_config(page_title="Career Prediction ML", layout="wide")

if "token" not in st.session_state:
    auth_page()
    st.stop()

st.sidebar.title("📊 Navigation")
page = st.sidebar.selectbox(
    "Menu",
    [
        "About",
        "Balance",
        "ML Prediction",
        "ML History",
        "Transactions",
        "Admin Panel",
    ],
)

# ---------------- ABOUT ----------------
if page == "About":
    st.title("🎓 Career Prediction System")
    st.markdown(
        """
        This platform predicts a student's future career based on:
        - Technical skills
        - Soft skills
        - Interests
        - Academic background
        
        Built using **FastAPI + ML + RabbitMQ + Streamlit**
        """
    )

# ---------------- BALANCE ----------------
elif page == "Balance":
    st.title("💰 Balance")
    r = get_balance(st.session_state.token)
    if r.status_code == 200:
        st.metric("Current Balance", r.json()["balance"])
    else:
        st.error(r.text)

# ---------------- ML REQUEST ----------------
elif page == "ML Prediction":
    st.title("🤖 Request Career Prediction")

    ml_model_id = st.text_input("ML Model ID (UUID)")

    payload = ml_input_form()

    if st.button("Send ML Request"):
        if not ml_model_id:
            st.error("Model ID required")
        else:
            r = create_ml_request(
                st.session_state.token, ml_model_id, payload
            )
            if r.status_code == 200:
                st.success(f"Request queued: {r.json()['request_id']}")
            else:
                st.error(r.text)

    st.divider()

    st.subheader("🔮 Get Prediction")
    ml_request_id = st.text_input("ML Request ID")

    if st.button("Get Prediction"):
        r = get_prediction(st.session_state.token, ml_request_id)
        if r.status_code == 200:
            st.success(f"Prediction: {r.json()['prediction']}")
        else:
            st.warning(r.text)

# ---------------- HISTORY ----------------
elif page == "ML History":
    st.title("📜 ML Request History")
    r = ml_request_history(st.session_state.token)
    if r.status_code == 200:
        for item in r.json():
            st.code(item)
    else:
        st.error(r.text)

elif page == "Transactions":
    st.title("📒 Transaction History")
    r = transaction_history(st.session_state.token)
    if r.status_code == 200:
        for item in r.json():
            st.code(item)
    else:
        st.error(r.text)

# ---------------- ADMIN ----------------
elif page == "Admin Panel":
    st.title("🛠 Admin Panel")

    user_id = st.text_input("User ID")
    amount = st.number_input("Amount", step=1)

    if st.button("Approve Deposit"):
        r = update_balance_admin(
            st.session_state.token, user_id, amount
        )
        if r.status_code == 200:
            st.success("Deposit successful")
        else:
            st.error(r.text)

    st.divider()
    st.subheader("User Transactions")

    if st.button("View User Transactions"):
        r = transaction_history_admin(
            st.session_state.token, user_id
        )
        if r.status_code == 200:
            for item in r.json():
                st.code(item)
        else:
            st.error(r.text)
