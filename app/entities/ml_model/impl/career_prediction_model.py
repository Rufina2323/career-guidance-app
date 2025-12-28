from dataclasses import dataclass, field
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder

import torch
import torch.nn as nn
import joblib


from entities.ml_model.ml_model import MLModel


class MLP(nn.Module):
    def __init__(self, input_dim=105, hidden_dim=50, num_classes=11):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, num_classes),
        )

    def forward(self, x):
        return self.net(x)


@dataclass(kw_only=True)
@dataclass
class CareerPredictionModel(MLModel):
    preprocessing_path: str
    preprocessing_pipeline: ColumnTransformer = field(init=False)

    label_encoder_path: str
    label_encoder: LabelEncoder = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()  # initialize model first
        self.preprocessing_pipeline = self.initialize_preprocessing()
        self.label_encoder = self.initialize_label_encoder()

    def initialize_model(self) -> torch.nn.Module:
        try:
            model = MLP(input_dim=105, num_classes=11)
            model.load_state_dict(torch.load(self.model_path))
            return model
        except FileNotFoundError:
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}") from e

    def initialize_preprocessing(self) -> ColumnTransformer:
        try:
            preprocessor = joblib.load(self.preprocessing_path)
            return preprocessor
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Preprocessor file not found: {self.preprocessing_path}"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load preprocessing pipeline: {e}") from e

    def initialize_label_encoder(self) -> LabelEncoder:
        try:
            label_encoder = joblib.load(self.label_encoder_path)
            return label_encoder
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Label encoder file not found: {self.label_encoder_path}"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load label encoder: {e}") from e
