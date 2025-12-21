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
        # TODO: add all data
        inference_data_model = InferenceDataModel(
            operating_systems_percentage=inference_data.operating_systems_percentage,
            algorithms_percentage=inference_data.algorithms_percentage,
            programming_concepts_percentage=inference_data.programming_concepts_percentage,
            software_engineering_percentage=inference_data.software_engineering_percentage,
            electronics_subjects_percentage=1,
            computer_architecture_percentage=1,
            mathematics_percentage=1,
            communication_skills_percentage=1,
            hours_working_per_day=1,
            logical_quotient_rating=1,
            hackathons=1,
            coding_skills_rating=1,
            public_speaking_points=1,
            can_work_long_time="a",
            self_learning_capability="a",
            extra_courses_did="a",
            certifications="a",
            workshops="a",
            talent_tests_taken="a",
            olympiads="a",
            reading_writing_skills="a",
            memory_capability_score="a",
            interested_subjects="a",
            interested_career_area="a",
            job_higher_studies="a",
            company_type_prefered="a",
            taken_inputs_from_elders="a",
            interested_in_games="a",
            interested_book_types="a",
            salary_range_expected="a",
            in_realtionship="a",
            behaviour="a",
            management_or_technical="a",
            worker_type="a",
            team_work="a",
            instrovert=True,
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
