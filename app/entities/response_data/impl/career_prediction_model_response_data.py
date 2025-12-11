from dataclasses import dataclass
from entities.response_data.response_data import ResponseData


@dataclass(kw_only=True)
class CareerPredictionModelResponseData(ResponseData):
    job_role_result: str
