from dataclasses import dataclass

from create_entites.inference_data.inference_data import InferenceDataCreateEntity


@dataclass
class CareerPredictionModelInferenceDataCreateEntity(InferenceDataCreateEntity):
    operating_systems_percentage: int
    algorithms_percentage: int
    programming_concepts_percentage: int
    software_engineering_percentage: int
