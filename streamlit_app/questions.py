import streamlit as st


# List of sections, each with a title and questions
QUESTION_SECTIONS = [
    {
        "section": "Technical Skills",
        "questions": [
            {
                "key": "operating_systems_percentage",
                "question": "How proficient are you in operating systems? (0-100)",
                "type": "number",
                "min": 0,
                "max": 100,
            },
            {
                "key": "algorithms_percentage",
                "question": "How proficient are you in algorithms? (0-100)",
                "type": "number",
                "min": 0,
                "max": 100,
            },
            {
                "key": "computer_networks_percentage",
                "question": "How proficient are you in computer networks? (0-100)",
                "type": "number",
                "min": 0,
                "max": 100,
            },
            {
                "key": "programming_concepts_percentage",
                "question": "How well do you understand programming concepts? (0-100)",
                "type": "number",
                "min": 0,
                "max": 100,
            },
            {
                "key": "software_engineering_percentage",
                "question": "How proficient are you in software engineering? (0-100)",
                "type": "number",
                "min": 0,
                "max": 100,
            },
        ],
    },
    {
        "section": "Other Skills",
        "questions": [
            {
                "key": "electronics_subjects_percentage",
                "question": "How well do you know electronics subjects? (0-100)",
                "type": "number",
                "min": 0,
                "max": 100,
            },
            {
                "key": "computer_architecture_percentage",
                "question": "How well do you understand computer architecture? (0-100)",
                "type": "number",
                "min": 0,
                "max": 100,
            },
            {
                "key": "mathematics_percentage",
                "question": "How strong are your mathematics skills? (0-100)",
                "type": "number",
                "min": 0,
                "max": 100,
            },
            {
                "key": "communication_skills_percentage",
                "question": "Rate your communication skills (0-100)",
                "type": "number",
                "min": 0,
                "max": 100,
            },
            {
                "key": "hackathons",
                "question": "How many hackathons have you participated in?",
                "type": "number",
                "min": 0,
                "max": 100,
            },
        ],
    },
    {
        "section": "Work & Study Habits",
        "questions": [
            {
                "key": "hours_working_per_day",
                "question": "How many hours can you work per day?",
                "type": "number",
                "min": 0,
                "max": 24,
            },
            {
                "key": "logical_quotient_rating",
                "question": "Rate your logical quotient (0-10)",
                "type": "number",
                "min": 0,
                "max": 10,
            },
            {
                "key": "coding_skills_rating",
                "question": "Rate your coding skills (0-10)",
                "type": "number",
                "min": 0,
                "max": 10,
            },
            {
                "key": "public_speaking_points",
                "question": "Rate your public speaking skills (0-10)",
                "type": "number",
                "min": 0,
                "max": 10,
            },
        ],
    },
    {
        "section": "Personal Traits",
        "questions": [
            {
                "key": "reading_writing_skills",
                "question": "How would you rate your reading and writing skills?",
                "type": "select",
                "options": ["Excellent", "Medium", "Poor"],
            },
            {
                "key": "memory_capability_score",
                "question": "How would you rate your memory capability?",
                "type": "select",
                "options": ["Excellent", "Medium", "Poor"],
            },
            {
                "key": "can_work_long_time",
                "question": "Can you work for long hours?",
                "type": "boolean",
            },
            {
                "key": "team_work",
                "question": "Can you work in a team?",
                "type": "boolean",
            },
            {
                "key": "self_learning_capability",
                "question": "Do you have good self-learning capability?",
                "type": "boolean",
            },
            {
                "key": "extra_courses_did",
                "question": "Have you done any extra courses?",
                "type": "boolean",
            },
            {
                "key": "talent_tests_taken",
                "question": "Have you taken any talent tests?",
                "type": "boolean",
            },
            {
                "key": "olympiads",
                "question": "Have you participated in any Olympiads?",
                "type": "boolean",
            },
            {
                "key": "taken_inputs_from_elders",
                "question": "Do you take advice from elders?",
                "type": "boolean",
            },
            {
                "key": "interested_in_games",
                "question": "Are you interested in games?",
                "type": "boolean",
            },
            {
                "key": "in_realtionship",
                "question": "Are you in a relationship?",
                "type": "boolean",
            },
            {
                "key": "introvert",
                "question": "Are you an introvert?",
                "type": "boolean",
            },
        ],
    },
    {
        "section": "Career & Preferences",
        "questions": [
            {
                "key": "behaviour",
                "question": "How would you describe your behaviour?",
                "type": "select",
                "options": ["Stubborn", "Gentle"],
            },
            {
                "key": "management_or_technical",
                "question": "Do you prefer management or technical work?",
                "type": "select",
                "options": ["Management", "Technical"],
            },
            {
                "key": "worker_type",
                "question": "What type of worker are you?",
                "type": "select",
                "options": ["Hard worker", "Smart worker"],
            },
            {
                "key": "job_higher_studies",
                "question": "Are you aiming for higher studies or a job?",
                "type": "select",
                "options": ["Higherstudies", "Job"],
            },
            {
                "key": "company_type_prefered",
                "question": "Which type of company would you prefer to work in?",
                "type": "select",
                "options": [
                    "Web Services",
                    "SAaS services",
                    "Sales And Marketing",
                    "Testing And Maintainance Services",
                    "Product Development",
                    "BPA",
                    "Service Based",
                    "Product Based",
                    "Cloud Services",
                    "Finance",
                ],
            },
            {
                "key": "salary_range_expected",
                "question": "Are you expecting a salary or aiming for work experience?",
                "type": "select",
                "options": ["Salary", "Work"],
            },
            {
                "key": "interested_subjects",
                "question": "Which subject are you most interested in?",
                "type": "select",
                "options": [
                    "Cloud Computing",
                    "Networks",
                    "Hacking",
                    "Computer Architecture",
                    "Programming",
                    "Parallel Computing",
                    "IoT",
                    "Data Engineering",
                    "Software Engineering",
                    "Management",
                ],
            },
            {
                "key": "interested_career_area",
                "question": "Which career area interests you the most?",
                "type": "select",
                "options": [
                    "System Developer",
                    "Business Process Analyst",
                    "Developer",
                    "Testing",
                    "Security",
                    "Cloud Computing",
                ],
            },
            {
                "key": "certifications",
                "question": "Which certification do you have?",
                "type": "select",
                "options": [
                    "Shell Programming",
                    "Machine Learning",
                    "App Development",
                    "Python",
                    "R Programming",
                    "Information Security",
                    "Hadoop",
                    "Distro Making",
                    "Full Stack",
                ],
            },
            {
                "key": "workshops",
                "question": "Which workshop have you attended?",
                "type": "select",
                "options": [
                    "Cloud Computing",
                    "Database Security",
                    "Web Technologies",
                    "Data Science",
                    "Testing",
                    "Hacking",
                    "Game Development",
                    "System Designing",
                ],
            },
            {
                "key": "interested_book_types",
                "question": "Which type of books do you prefer?",
                "type": "select",
                "options": [
                    "Prayer books",
                    "Childrens",
                    "Travel",
                    "Romance",
                    "Cookbooks",
                    "Self help",
                    "Drama",
                    "Math",
                    "Religion-Spirituality",
                    "Anthology",
                    "Trilogy",
                    "Autobiographies",
                    "Mystery",
                    "Diaries",
                    "Journals",
                    "History",
                    "Art",
                    "Dictionaries",
                    "Horror",
                    "Encyclopedias",
                    "Action and Adventure",
                    "Fantasy",
                    "Comics",
                    "Science fiction",
                    "Series",
                    "Guide",
                    "Biographies",
                    "Health",
                    "Satire",
                    "Science",
                    "Poetry",
                ],
            },
        ],
    },
]


def ml_input_form():
    """Render all sections with questions. Returns a dict of answers."""
    data = {}

    for section in QUESTION_SECTIONS:
        st.markdown(f"## {section['section']}")
        for q in section["questions"]:
            if q["type"] == "number":
                data[q["key"]] = st.number_input(
                    q["question"],
                    min_value=q.get("min", 0),
                    max_value=q.get("max", 100),
                    value=q.get("default", 0),
                )
            elif q["type"] == "boolean":
                data[q["key"]] = (
                    st.radio(q["question"], ["Yes", "No"], horizontal=True) == "Yes"
                )
            elif q["type"] == "select":
                data[q["key"]] = st.selectbox(
                    q["question"],
                    q["options"],
                )
    return data
