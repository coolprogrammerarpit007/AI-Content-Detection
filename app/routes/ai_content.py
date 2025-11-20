from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.content_schema import ContentRequest, ContentResponse
from app.services.ai_service import check_content
from app.core.database import get_db

router = APIRouter()


@router.post("/check-content", response_model=ContentResponse)
async def check_ai_content(payload: ContentRequest, db: AsyncSession = Depends(get_db)):
    return await check_content(payload.text_content, db)
