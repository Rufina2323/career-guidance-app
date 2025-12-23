from uuid import uuid4
from unittest.mock import patch
from models.ml_request import Status
from services.ml_request_service import MLRequestService


def test_change_ml_request_status(ml_request_service: MLRequestService) -> None:
    ml_request_id = uuid4()
    status = Status.COMPLETED

    with patch.object(ml_request_service.ml_request_repository, "change_ml_request_status") as mock_change_status:
        ml_request_service.change_ml_request_status(ml_request_id, status)
        mock_change_status.assert_called_once_with(ml_request_id, status)
