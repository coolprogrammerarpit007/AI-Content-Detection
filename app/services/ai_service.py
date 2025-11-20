import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content_log import ContentLog
from app.core.config import settings
from app.schemas.content_schema import AIContentData

async def check_content(text: str, db: AsyncSession):
    try:
        url = settings.WATSON_API_URL
        headers = {
            "Authorization": f"Bearer {settings.WATSON_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "version": 4.11,
            "sentences": True,
            "language": "en"
        }

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            return {
                "status": False,
                "message": "AI content check failed",
                "data": None
            }

        data = response.json()
        # Extract fields
        new_log = ContentLog(
            status=data.get("status"),
            human_score=data.get("score"),
            readability_score=data.get("readability_score"),
            credits_used=data.get("credits_used"),
            credits_remaining=data.get("credits_remaining"),
            language=data.get("language"),
        )

        db.add(new_log)
        await db.commit()
        await db.refresh(new_log)

        return {
            "status": True,
            "message": "AI check completed",
            "data": AIContentData(**data)
        }

    except Exception as e:
        return {
            "status": False,
            "message": str(e),
            "data": None
        }