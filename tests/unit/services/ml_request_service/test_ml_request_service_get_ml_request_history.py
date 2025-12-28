from uuid import uuid4
from unittest.mock import MagicMock, patch
from services.ml_request_service import MLRequestService


def test_get_ml_request_history(ml_request_service: MLRequestService) -> None:
    user_id = uuid4()
    ml_request1 = MagicMock()
    ml_request2 = MagicMock()
    ml_request1.timestamp = 1
    ml_request2.timestamp = 2

    with patch.object(
        ml_request_service.ml_request_repository,
        "get_ml_request_history",
        return_value=[ml_request1, ml_request2],
    ) as mock_history:
        result = ml_request_service.get_ml_request_history(user_id)

        mock_history.assert_called_once_with(user_id)
        # Should be sorted by timestamp descending
        assert result == [ml_request2, ml_request1]
