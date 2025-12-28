from uuid import uuid4
from unittest.mock import patch

from entities.inference_data.impl.career_prediction_model_inference_data import (
    CareerPredictionModelInferenceData,
)
import pytest

from services.inference_data_service import InferenceDataService


def test_get_data(inference_data_service: InferenceDataService) -> None:
    inference_data_id = uuid4()
    inference_data = CareerPredictionModelInferenceData(
        operating_systems_percentage=0,
        algorithms_percentage=0,
        programming_concepts_percentage=0,
        computer_networks_percentage=0,
        software_engineering_percentage=0,
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
        introvert=True,
    )

    with patch.object(
        inference_data_service.inference_data_repository,
        "get_data",
        return_value=inference_data,
    ) as mock_get_data:
        result = inference_data_service.get_data(inference_data_id)

        mock_get_data.assert_called_once_with(inference_data_id)
        assert result == inference_data
