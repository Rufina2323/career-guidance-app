from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import torch


@dataclass(kw_only=True)
class MLModel(ABC):
    model_id: int
    name: str
    request_cost: float
    model_path: str
    model: torch.nn.Module = field(init=False)

    def __post_init__(self) -> None:
        self.model = self.initialize_model()

    @abstractmethod
    def initialize_model(self) -> torch.nn.Module:
        pass
