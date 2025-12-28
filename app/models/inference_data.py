from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid
from entities.inference_data.impl.career_prediction_model_inference_data import (
    CareerPredictionModelInferenceData as CareerPredictionModelInferenceDataEntity,
)
from entities.inference_data.inference_data import InferenceData as InferenceDataEntity

if TYPE_CHECKING:
    from models.ml_request import MLRequest


class InferenceData(SQLModel, table=True):
    __tablename__ = "inference_data"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
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

    ml_request: "MLRequest" = Relationship(back_populates="inference_data")

    @classmethod
    def to_domain(cls, inference_data_model: "InferenceData") -> InferenceDataEntity:
        return CareerPredictionModelInferenceDataEntity(
            operating_systems_percentage=inference_data_model.operating_systems_percentage,
            algorithms_percentage=inference_data_model.algorithms_percentage,
            programming_concepts_percentage=inference_data_model.programming_concepts_percentage,
            computer_networks_percentage=inference_data_model.computer_networks_percentage,
            software_engineering_percentage=inference_data_model.software_engineering_percentage,
            electronics_subjects_percentage=inference_data_model.electronics_subjects_percentage,
            computer_architecture_percentage=inference_data_model.computer_architecture_percentage,
            mathematics_percentage=inference_data_model.mathematics_percentage,
            communication_skills_percentage=inference_data_model.communication_skills_percentage,
            hours_working_per_day=inference_data_model.hours_working_per_day,
            logical_quotient_rating=inference_data_model.logical_quotient_rating,
            hackathons=inference_data_model.hackathons,
            coding_skills_rating=inference_data_model.coding_skills_rating,
            public_speaking_points=inference_data_model.public_speaking_points,
            can_work_long_time=inference_data_model.can_work_long_time,
            self_learning_capability=inference_data_model.self_learning_capability,
            extra_courses_did=inference_data_model.extra_courses_did,
            certifications=inference_data_model.certifications,
            workshops=inference_data_model.workshops,
            talent_tests_taken=inference_data_model.talent_tests_taken,
            olympiads=inference_data_model.olympiads,
            reading_writing_skills=inference_data_model.reading_writing_skills,
            memory_capability_score=inference_data_model.memory_capability_score,
            interested_subjects=inference_data_model.interested_subjects,
            interested_career_area=inference_data_model.interested_career_area,
            job_higher_studies=inference_data_model.job_higher_studies,
            company_type_prefered=inference_data_model.company_type_prefered,
            taken_inputs_from_elders=inference_data_model.taken_inputs_from_elders,
            interested_in_games=inference_data_model.interested_in_games,
            interested_book_types=inference_data_model.interested_book_types,
            salary_range_expected=inference_data_model.salary_range_expected,
            in_realtionship=inference_data_model.in_realtionship,
            behaviour=inference_data_model.behaviour,
            management_or_technical=inference_data_model.management_or_technical,
            worker_type=inference_data_model.worker_type,
            team_work=inference_data_model.team_work,
            introvert=inference_data_model.introvert,
        )
