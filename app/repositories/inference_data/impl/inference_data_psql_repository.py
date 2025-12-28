import uuid
from create_entites.inference_data.inference_data import InferenceDataCreateEntity
from sqlmodel import Session, select
from database.engine import engine

from sqlalchemy.exc import NoResultFound
from entities.inference_data.inference_data import InferenceData
from models.inference_data import InferenceData as InferenceDataModel
from repositories.inference_data.repository import InferenceDataRepository


class InferenceDataPSQLRepository(InferenceDataRepository):
    def __init__(self):
        self.session_maker = Session

    def add_data(self, inference_data: InferenceDataCreateEntity) -> uuid.UUID:
        inference_data_model = InferenceDataModel(
            operating_systems_percentage=inference_data.operating_systems_percentage,
            algorithms_percentage=inference_data.algorithms_percentage,
            programming_concepts_percentage=inference_data.programming_concepts_percentage,
            computer_networks_percentage=inference_data.computer_networks_percentage,
            software_engineering_percentage=inference_data.software_engineering_percentage,
            electronics_subjects_percentage=inference_data.electronics_subjects_percentage,
            computer_architecture_percentage=inference_data.computer_architecture_percentage,
            mathematics_percentage=inference_data.mathematics_percentage,
            communication_skills_percentage=inference_data.communication_skills_percentage,
            hours_working_per_day=inference_data.hours_working_per_day,
            logical_quotient_rating=inference_data.logical_quotient_rating,
            hackathons=inference_data.hackathons,
            coding_skills_rating=inference_data.coding_skills_rating,
            public_speaking_points=inference_data.public_speaking_points,
            can_work_long_time=inference_data.can_work_long_time,
            self_learning_capability=inference_data.self_learning_capability,
            extra_courses_did=inference_data.extra_courses_did,
            certifications=inference_data.certifications,
            workshops=inference_data.workshops,
            talent_tests_taken=inference_data.talent_tests_taken,
            olympiads=inference_data.olympiads,
            reading_writing_skills=inference_data.reading_writing_skills,
            memory_capability_score=inference_data.memory_capability_score,
            interested_subjects=inference_data.interested_subjects,
            interested_career_area=inference_data.interested_career_area,
            job_higher_studies=inference_data.job_higher_studies,
            company_type_prefered=inference_data.company_type_prefered,
            taken_inputs_from_elders=inference_data.taken_inputs_from_elders,
            interested_in_games=inference_data.interested_in_games,
            interested_book_types=inference_data.interested_book_types,
            salary_range_expected=inference_data.salary_range_expected,
            in_realtionship=inference_data.in_realtionship,
            behaviour=inference_data.behaviour,
            management_or_technical=inference_data.management_or_technical,
            worker_type=inference_data.worker_type,
            team_work=inference_data.team_work,
            introvert=inference_data.introvert,
        )

        with self.session_maker(engine) as session:
            session.add(inference_data_model)
            session.commit()
            return inference_data_model.id

    def get_data(self, inference_data_id: uuid.UUID) -> InferenceData | None:
        with self.session_maker(engine) as session:
            try:
                statement = select(InferenceDataModel).where(
                    InferenceDataModel.id == inference_data_id
                )
                psql_inference_data = session.exec(statement).one()
                return InferenceDataModel.to_domain(psql_inference_data)

            except NoResultFound:
                return None
