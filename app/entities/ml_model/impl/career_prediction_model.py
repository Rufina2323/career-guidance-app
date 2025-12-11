from dataclasses import dataclass, field

import torch


from entities.ml_model.ml_model import MLModel


@dataclass
class CareerPredictionModel(MLModel):
    preprocessing_path: str
    preprocessing_pipeline: dict = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()  # initialize model first
        try:
            self.preprocessing_pipeline = self.initialize_preprocessing()
        except Exception:
            self.preprocessing_pipeline = {}

    def initialize_model(self) -> torch.nn.Module:
        pass

    def initialize_preprocessing(self) -> dict:
        pass
