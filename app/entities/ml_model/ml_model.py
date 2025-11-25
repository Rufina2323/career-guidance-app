from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from entities.inference_data.inference_data import InferenceData
from entities.response.response import Response
import torch


@dataclass
class MLModel(ABC):
    model_id: int
    name: str
    request_cost: float
    model_path: str
    model: torch.nn.Module = field(init=False)

    def __post_init__(self) -> None:
        try:
            self.model = self.initialize_model()
        except Exception:
            self.model = None

    @abstractmethod
    def initialize_model(self) -> torch.nn.Module:
        pass

    @abstractmethod
    def predict(self, inference_data: InferenceData) -> Response:
        pass
