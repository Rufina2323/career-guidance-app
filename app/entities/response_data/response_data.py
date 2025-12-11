from abc import ABC
from dataclasses import dataclass


@dataclass(kw_only=True)
class ResponseData(ABC):
    pass
