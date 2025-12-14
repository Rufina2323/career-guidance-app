from pydantic import BaseModel


class InderenceDataDTO(BaseModel):
    operating_systems_percentage: int
    algorithms_percentage: int
    programming_concepts_percentage: int
    software_engineering_percentage: int
