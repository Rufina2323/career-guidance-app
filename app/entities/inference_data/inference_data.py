from abc import ABC
from dataclasses import dataclass


@dataclass(kw_only=True)
@dataclass
class InferenceData(ABC):
    pass
