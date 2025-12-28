from pydantic import BaseModel


class ResponseDataDTO(BaseModel):
    job_role_result: str
