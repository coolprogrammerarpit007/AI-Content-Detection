from pydantic import BaseModel


class SubmitRequest(BaseModel):
    text: str


class DetectionResponse(BaseModel):
    scan_id: str
    ai_score: float
    human_score: float