from dataclasses import dataclass, field
from datetime import datetime

from entities.inference_data.inference_data import InferenceData
from entities.ml_model.ml_model import MLModel
from entities.person.person import Person
from entities.response_data.response_data import ResponseData


@dataclass
class MLRequest:
    person: Person
    ml_model: MLModel
    inference_data: InferenceData
    response_data: ResponseData
    status: str
    timestamp: datetime
