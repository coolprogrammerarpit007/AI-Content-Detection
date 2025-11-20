from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.content_schema import ContentRequest, ContentResponse
from app.services.ai_service import check_content,detect_category
from app.core.database import get_db

router = APIRouter()


@router.post("/check-content", response_model=ContentResponse)
async def check_ai_content(payload: ContentRequest, db: AsyncSession = Depends(get_db)):
    return await check_content(payload.text_content, db)


# -------------------
# CATEGORY DETECTION
# -------------------
@router.post("/ai-content-category")
async def ai_content_category(payload: ContentRequest):
    category = await detect_category(payload.text_content)
    return {
        "status": True,
        "message": "Category detected successfully",
        "category": category
    }