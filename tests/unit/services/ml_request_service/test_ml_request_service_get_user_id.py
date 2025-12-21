from uuid import uuid4
from unittest.mock import patch
from services.ml_request_service import MLRequestService


def test_get_user_id(ml_request_service: MLRequestService) -> None:
    ml_request_id = uuid4()
    user_id = uuid4()

    with patch.object(ml_request_service.ml_request_repository, "get_user_id", return_value=user_id) as mock_get_user_id:
        result = ml_request_service.get_user_id(ml_request_id)
        mock_get_user_id.assert_called_once_with(ml_request_id)
        assert result == user_id
