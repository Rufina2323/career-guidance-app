import streamlit as st


def ml_input_form():
    st.subheader("🧠 Career Prediction Survey")

    data = {}
    int_fields = [
        "operating_systems_percentage",
        "algorithms_percentage",
        "programming_concepts_percentage",
        "software_engineering_percentage",
        "electronics_subjects_percentage",
        "computer_architecture_percentage",
        "mathematics_percentage",
        "communication_skills_percentage",
        "hours_working_per_day",
        "logical_quotient_rating",
        "hackathons",
        "coding_skills_rating",
        "public_speaking_points",
    ]

    for f in int_fields:
        data[f] = st.number_input(f, min_value=0, max_value=100)

    str_fields = [
        "can_work_long_time",
        "self_learning_capability",
        "extra_courses_did",
        "certifications",
        "workshops",
        "talent_tests_taken",
        "olympiads",
        "reading_writing_skills",
        "memory_capability_score",
        "interested_subjects",
        "interested_career_area",
        "job_higher_studies",
        "company_type_prefered",
        "taken_inputs_from_elders",
        "interested_in_games",
        "interested_book_types",
        "salary_range_expected",
        "in_realtionship",
        "behaviour",
        "management_or_technical",
        "worker_type",
        "team_work",
    ]

    for f in str_fields:
        data[f] = st.text_input(f)

    data["instrovert"] = st.checkbox("Introvert")

    return data
