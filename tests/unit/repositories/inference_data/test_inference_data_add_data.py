from uuid import uuid4
from unittest.mock import patch, MagicMock

from repositories.inference_data.impl.inference_data_psql_repository import (
    InferenceDataPSQLRepository,
)
from create_entites.inference_data.impl.career_prediction_model_inference_data import CareerPredictionModelInferenceDataCreateEntity
from models.inference_data import InferenceData as InferenceDataModel


def test_add_data(inference_data_psql_repository: InferenceDataPSQLRepository) -> None:
    inference_data_id = uuid4()

    inference_data = CareerPredictionModelInferenceDataCreateEntity(
        operating_systems_percentage=1,
        algorithms_percentage=2,
        programming_concepts_percentage=3,
        software_engineering_percentage=4,
        electronics_subjects_percentage=0,
        computer_architecture_percentage=0,
        mathematics_percentage=0,
        communication_skills_percentage=0,
        hours_working_per_day=0,
        logical_quotient_rating=0,
        hackathons=0,
        coding_skills_rating=0,
        public_speaking_points=0,
        can_work_long_time="yes",
        self_learning_capability="yes",
        extra_courses_did="yes",
        certifications="shell programming",
        workshops="cloud computing",
        talent_tests_taken="no",
        olympiads="no",
        reading_writing_skills="poor",
        memory_capability_score="medium",
        interested_subjects="networks",
        interested_career_area="system developer",
        job_higher_studies="higherstudies",
        company_type_prefered="Web Services",
        taken_inputs_from_elders="no",
        interested_in_games="no",
        interested_book_types="Prayer books",
        salary_range_expected="salary",
        in_realtionship="no",
        behaviour="stubborn",
        management_or_technical="Management",
        worker_type="hard worker",
        team_work="yes",
        instrovert=True
    )

    with patch.object(
        inference_data_psql_repository, "session_maker"
    ) as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value.__enter__.return_value = mock_session

        mock_model = MagicMock(spec=InferenceDataModel)
        mock_model.id = inference_data_id

        with patch(
            "repositories.inference_data.impl.inference_data_psql_repository.InferenceDataModel",
            return_value=mock_model,
        ) as mock_model_cls:

            result = inference_data_psql_repository.add_data(inference_data)

            mock_model_cls.assert_called_once()
            mock_session.add.assert_called_once_with(mock_model)
            mock_session.commit.assert_called_once()
            assert result == inference_data_id
