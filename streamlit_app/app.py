import streamlit as st
from api import *
from auth import auth_page
from questions import ml_input_form
import pandas as pd
from questions import QUESTION_SECTIONS


# Flatten all questions to a dictionary {key: question_text}
QUESTION_MAP = {}
SECTION_ORDER = []

# --- Apply mappings for categorical fields ---
mapping_dict = {
    "job_higher_studies": {"Higherstudies": 1, "Job": 0},
    "salary_range_expected": {"Salary": 1, "Work": 0},
    "behaviour": {"Stubborn": 1, "Gentle": 0},
    "management_or_technical": {"Management": 1, "Technical": 0},
    "worker_type": {"Hard worker": 1, "Smart worker": 0},
    "reading_writing_skills": {"Excellent": 2, "Medium": 1, "Poor": 0},
    "memory_capability_score": {"Excellent": 2, "Medium": 1, "Poor": 0},
}

# Create reverse mapping
reverse_mapping_dict = {
    key: {v: k for k, v in value.items()} for key, value in mapping_dict.items()
}

# Convert checkboxes (True/False) to 1/0
checkbox_fields = [
    "can_work_long_time",
    "self_learning_capability",
    "extra_courses_did",
    "talent_tests_taken",
    "olympiads",
    "taken_inputs_from_elders",
    "interested_in_games",
    "in_realtionship",
    "introvert",
]

for section in QUESTION_SECTIONS:
    SECTION_ORDER.append(section["section"])
    for q in section["questions"]:
        QUESTION_MAP[q["key"]] = (section["section"], q["question"])


def group_by_section(data_dict):
    """Group a flat dict of keys into sections using QUESTION_MAP"""
    sections_data = {section: {} for section in SECTION_ORDER}

    for key, value in data_dict.items():
        section, question = QUESTION_MAP.get(key)
        sections_data[section][question] = value
    return sections_data


st.set_page_config(page_title="Career Prediction ML", layout="wide")

if "token" not in st.session_state:
    auth_page()
    st.stop()

st.sidebar.title("📊 Navigation")
import streamlit as st

# Initialize session_state to store the current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "About"

# Sidebar buttons
if st.sidebar.button("About"):
    st.session_state.current_page = "About"
if st.sidebar.button("Balance"):
    st.session_state.current_page = "Balance"
if st.sidebar.button("ML Request"):
    st.session_state.current_page = "ML Request"
if st.sidebar.button("ML History"):
    st.session_state.current_page = "ML History"
if st.sidebar.button("Transactions"):
    st.session_state.current_page = "Transactions"

if st.session_state.user_role == "admin":
    if st.sidebar.button("Admin Panel"):
        st.session_state.current_page = "Admin Panel"

# Render the selected page
page = st.session_state.current_page

if "ml_request_id" not in st.session_state:
    st.session_state.ml_request_id = None

# ---------------- ABOUT ----------------
if page == "About":
    st.title("🎓 Career Prediction System")

    st.markdown("""
    Welcome to the **Career Prediction Platform**! This system helps students and professionals understand their career path based on various skills, preferences, and experiences.
    """)

    st.markdown("### 🔹 Features")
    st.markdown("""
    - **Career Prediction**: Predicts suitable career paths based on technical, soft skills, and interests.
    - **ML Request History**: View your past prediction requests and results.
    - **Balance & Transactions**: Track credits for ML requests and manage deposits.
    - **Admin Panel** (for admins): Approve/reject deposit requests and view user transactions.
    """)

    st.markdown("### 🔹 How It Works")
    st.markdown("""
    1. Fill out a detailed survey about your skills, education, and interests.
    2. Choose an ML model to run a career prediction.
    3. Submit the request; the system queues and processes it using **FastAPI** and **RabbitMQ**.
    4. View results in the **ML History** section.
    5. Your inputs are securely stored and used only for prediction purposes.
    """)

    st.markdown("### 🔹 Notes")
    st.markdown("""
    - ML predictions are **guidance only**; they do not guarantee career outcomes.
    - Ensure all survey fields are filled as accurately as possible for best predictions.
    - Admin users have additional capabilities like managing deposits and reviewing user activity.
    """)

    st.markdown("### 🔹 Get Started")
    st.markdown("""
    Use the sidebar to navigate:
    - **Balance**: Manage your account and deposits
    - **ML Request**: Submit new career prediction requests
    - **ML History**: Review past predictions
    - **Transactions**: Track your transactions
    """)

# ---------------- BALANCE ----------------
elif page == "Balance":
    st.title("💰 Balance")
    r = get_balance(st.session_state.token)
    if r.status_code == 200:
        st.metric("Current Balance", r.json()["balance"])
    else:
        st.error(r.text)

    st.title("💰 Request a Deposit")
    amount = st.number_input(
        "Enter deposit amount:", min_value=1.0, value=100.0, step=1.0, format="%.2f"
    )

    if st.button("Submit Deposit Request"):
        if amount <= 0:
            st.error("Amount must be greater than 0")
        else:
            r = request_deposit_user(st.session_state.token, amount)
            if r.status_code == 200:
                data = r.json()
                st.success(f"Deposit request created! ✅")
            else:
                st.error(f"Failed to create deposit request: {r.text}")

# ---------------- ML REQUEST ----------------
elif page == "ML Request":
    st.title("🤖 Request Career Prediction")

    # Get list of models
    models = get_models(st.session_state.token)

    if models:
        # Build display labels
        model_options = [f"{m['name']} (Cost: ${m['cost']})" for m in models]

        # Let user select a model
        selected_index = st.selectbox(
            "Choose ML model",
            range(len(models)),
            format_func=lambda x: model_options[x],
        )

        # Get the corresponding UUID for API request
        ml_model_id = models[selected_index]["id"]
    else:
        ml_model_id = None

    payload = ml_input_form()  # Collect raw form data

    if st.button("Send ML Request"):
        if not ml_model_id:
            st.error("Model ID required")
        else:
            # Convert to DataFrame for transformation
            df = pd.DataFrame([payload])

            for key, map_dict in mapping_dict.items():
                df[key] = df[key].map(map_dict)

            for field in checkbox_fields:
                df[field] = df[field].astype(int)
            transformed_payload = df.to_dict(orient="records")[0]

            r = create_ml_request(
                st.session_state.token, ml_model_id, transformed_payload
            )

            if r.status_code == 200:
                st.success(f"ML Request queued")
                st.session_state.ml_request_id = r.json()["request_id"]
            else:
                try:
                    error_msg = r.json().get("detail", r.text)
                except ValueError:
                    error_msg = r.text

                st.error(f"❌ {error_msg}")

    st.divider()

    st.subheader("🔮 Get Prediction")
    # ml_request_id = current_ml_request_id

    if st.button("Get Prediction"):
        if not st.session_state.ml_request_id:
            st.warning("Please send ML request first")
        else:
            r = get_prediction(st.session_state.token, st.session_state.ml_request_id)
            st.session_state.ml_request_id = None
            if r.status_code == 200:
                st.success(f"Career Prediction: {r.json()['prediction']}")
            else:
                st.warning(r.text)

# ---------------- HISTORY ----------------
elif page == "ML History":
    st.title("📜 ML Request History")

    r = ml_request_history(st.session_state.token)

    if r.status_code != 200:
        st.error(r.text)
    else:
        data = r.json()

        if not data:
            st.info("No ML requests found.")
        else:
            # -------- TABLE VIEW (summary only) --------
            table_rows = []
            for idx, item in enumerate(data):
                table_rows.append(
                    {
                        "ID": idx + 1,
                        "Model": item["ml_model_name"],
                        "Cost": item["ml_model_request_cost"],
                        "Status": item["status"],
                        "Timestamp": item["timestamp"],
                    }
                )

            df = pd.DataFrame(table_rows)
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])

            st.subheader("📊 Requests Overview")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            st.divider()

            # -------- DETAILS VIEW --------
            st.subheader("🔍 Request Details")

            for idx, item in enumerate(data):
                with st.expander(
                    f"🧠 {item['ml_model_name']} | "
                    f"{item['status']} | "
                    f"{item['timestamp']}"
                ):
                    col1, col2 = st.columns(2)

                    # Left column: Prediction Result
                    with col1:
                        st.markdown("### 🎯 Prediction Result")
                        response_data = item["response_data"]
                        for key, value in response_data.items():
                            question = QUESTION_MAP.get(
                                key, key
                            )
                            st.write(f"**{question}:** {value}")

                    # Right column: Input (Inference Data)
                    with col2:
                        st.markdown("### 📥 Input (Inference Data)")
                        inference_data = item["inference_data"]
                        df = pd.DataFrame([inference_data])

                        for key, map_dict in reverse_mapping_dict.items():
                            df[key] = df[key].map(map_dict)

                        for field in checkbox_fields:
                            df[field] = df[field].astype(bool)

                        inference_data = df.to_dict(orient="records")[0]
                        sections = group_by_section(inference_data)
                        for section_name, questions in sections.items():
                            st.markdown(f"#### {section_name}")
                            for question, value in questions.items():
                                st.write(f"**{question}:** {value}")

    # ---------------- TRANSACTIONS ----------------
elif page == "Transactions":
    st.title("📒 Transaction History")

    r = transaction_history(st.session_state.token)

    if r.status_code == 200:
        data = r.json()

        if not data:
            st.info("No transactions found.")
        else:
            df = pd.DataFrame(data)

            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp", ascending=False)

            df.rename(
                columns={
                    "transaction_type": "Type",
                    "amount": "Amount",
                    "timestamp": "Timestamp",
                },
                inplace=True,
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.error(r.text)


elif page == "Admin Panel":
    st.title("💰 Deposit Requests (Admin)")

    r = get_deposit_requests_admin(st.session_state.token)

    if r.status_code != 200:
        st.error(r.text)
    else:
        deposit_requests = r.json()

        if not deposit_requests:
            st.info("No deposit requests in queue.")
        else:
            for req in deposit_requests:
                deposit_id = req["deposit_id"]
                st.markdown(
                    f"**User:** {req['username']}  |  "
                    f"**Amount:** {req['amount']}  |  "
                    f"**Timestamp:** {req['timestamp']}"
                )

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(f"✅ Approve", key=f"approve_{deposit_id}"):
                        res = approve_deposit(st.session_state.token, deposit_id)
                        if res.status_code == 200:
                            st.success(f"Deposit approved for {req['username']}")
                        else:
                            st.error(res.text)

                with col2:
                    if st.button(f"❌ Reject", key=f"reject_{deposit_id}"):
                        res = reject_deposit(st.session_state.token, deposit_id)
                        if res.status_code == 200:
                            st.warning(f"Deposit rejected for {req['username']}")
                        else:
                            st.error(res.text)

                st.markdown("---")

    st.title("🛠️ User Transaction History")

    users_response = get_all_users(st.session_state.token)

    if users_response.status_code != 200:
        st.error(users_response.text)
    else:
        users = users_response.json()

        if not users:
            st.info("No users found.")
        else:
            # Build dropdown options
            user_map = {f"{u['username']} ({u['role']})": u["user_id"] for u in users}

            selected_label = st.selectbox(
                "Select user",
                options=list(user_map.keys()),
            )

            selected_user_id = user_map[selected_label]

            r = transaction_history_admin(st.session_state.token, selected_user_id)

            if r.status_code == 200:
                data = r.json()

                if not data:
                    st.info("No transactions found for this user.")
                else:
                    df = pd.DataFrame(data)
                    df["timestamp"] = pd.to_datetime(df["timestamp"])
                    df = df.sort_values("timestamp", ascending=False)

                    df.rename(
                        columns={
                            "transaction_type": "Type",
                            "amount": "Amount",
                            "timestamp": "Timestamp",
                        },
                        inplace=True,
                    )

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                    )
            else:
                st.error(r.text)
