from pydantic import BaseModel


class UpdateBalanceDTO(BaseModel):
    amount: float
    