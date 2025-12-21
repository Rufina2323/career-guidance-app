from uuid import uuid4
from unittest.mock import patch
from models.ml_request import Status
from services.ml_request_service import MLRequestService


def test_get_ml_request_status(ml_request_service: MLRequestService) -> None:
    ml_request_id = uuid4()
    status = Status.RUNNING

    with patch.object(ml_request_service.ml_request_repository, "get_ml_request_status", return_value=status) as mock_get_status:
        result = ml_request_service.get_ml_request_status(ml_request_id)
        mock_get_status.assert_called_once_with(ml_request_id)
        assert result == status
