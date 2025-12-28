from dataclasses import dataclass
from entities.inference_data.inference_data import InferenceData


@dataclass(kw_only=True)
class CareerPredictionModelInferenceData(InferenceData):
    operating_systems_percentage: int
    algorithms_percentage: int
    programming_concepts_percentage: int
    computer_networks_percentage: int
    software_engineering_percentage: int
    electronics_subjects_percentage: int
    computer_architecture_percentage: int
    mathematics_percentage: int
    communication_skills_percentage: int
    hours_working_per_day: int
    logical_quotient_rating: int
    hackathons: int
    coding_skills_rating: int
    public_speaking_points: int
    can_work_long_time: int
    self_learning_capability: int
    extra_courses_did: int
    certifications: str
    workshops: str
    talent_tests_taken: int
    olympiads: int
    reading_writing_skills: int
    memory_capability_score: int
    interested_subjects: str
    interested_career_area: str
    job_higher_studies: int
    company_type_prefered: str
    taken_inputs_from_elders: int
    interested_in_games: int
    interested_book_types: str
    salary_range_expected: int
    in_realtionship: int
    behaviour: int
    management_or_technical: int
    worker_type: int
    team_work: int
    introvert: int
