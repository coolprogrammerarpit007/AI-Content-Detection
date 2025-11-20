from typing import Optional, List
from pydantic import BaseModel


class ContentRequest(BaseModel):
    text_content: str


class SentenceScore(BaseModel):
    text: Optional[str] = None
    score: Optional[float] = None
    length: Optional[int] = None


class AttackDetected(BaseModel):
    zero_width_space: Optional[bool] = None
    homoglyph_attack: Optional[bool] = None


class AIContentData(BaseModel):
    status: Optional[int] = None
    score: Optional[float] = None
    sentences: Optional[List[SentenceScore]] = None
    input: Optional[str] = None
    attack_detected: Optional[AttackDetected] = None
    readability_score: Optional[float] = None
    credits_used: Optional[int] = None
    credits_remaining: Optional[int] = None
    version: Optional[str] = None
    language: Optional[str] = None


class ContentResponse(BaseModel):
    status: bool
    message: str
    data: Optional[AIContentData] = None
