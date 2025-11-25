from dataclasses import dataclass, field
from datetime import datetime

from entities.inference_data.inference_data import InferenceData
from entities.ml_model.ml_model import MLModel
from entities.person.person import Person
from entities.response.response import Response


@dataclass
class MLRequest:
    user: Person
    ml_model: MLModel
    input_data: InferenceData
    result: Response
    status: str
    timestamp: datetime = field(default_factory=datetime.now)
    credits_used: float = 0.0

    def execute(self) -> Response:
        """Run the prediction using the MLModel."""
        self.result = self.ml_model.predict(self.input_data)
        return self.result
