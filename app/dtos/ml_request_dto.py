from datetime import datetime
import uuid
from dtos.inference_data_dto import InferenceDataDTO
from dtos.response_data_dto import ResponseDataDTO
from pydantic import BaseModel


class MLRequestDTO(BaseModel):
    ml_model_name: str
    ml_model_request_cost: float
    inference_data: InferenceDataDTO
    response_data: ResponseDataDTO
    status: str
    timestamp: datetime
