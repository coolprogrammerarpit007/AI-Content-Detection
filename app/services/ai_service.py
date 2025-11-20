import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content_log import ContentLog
from app.core.config import settings
from app.schemas.content_schema import AIContentData
from app.core.logger import logger
from app.ml.text_classifier import classify_text



def validate_text(clean_text: str):
    # 1. Empty string check
    if clean_text.strip() == "":
        logger.error("❌ Empty text received from client.")
        return False

    # 2. Minimum text length (at least 300 chars)
    if len(clean_text) < 300:
        logger.error("❌ Text too short for AI detection.")
        return False

    # 3. Maximum length check
    if len(clean_text) > 150000:
        logger.error("❌ Text exceeds maximum allowed size (150K chars).")
        return False

    # 4. Reject only numbers
    if clean_text.isnumeric():
        logger.error("❌ Only numbers were provided.")
        return False

    # 5. Reject too many repeated characters (spam)
    if len(set(clean_text)) <= 3:
        logger.error("❌ Spam-like repetitive characters detected.")
        return False

    # 6. Reject script/code injection
    forbidden_patterns = ["<script", "</script>", "<?php", "SELECT *", "DROP TABLE", "INSERT INTO"]
    if any(p.lower() in clean_text.lower() for p in forbidden_patterns):
        logger.error("❌ Potentially harmful or unsafe content detected!")
        return False

    # 7. Reject emoji-only text
    if all(not c.isalnum() for c in clean_text):
        logger.error("❌ Emoji or symbol-only text detected!")
        return False

    return True

async def check_content(text: str, db: AsyncSession):
    try:
        url = settings.WATSON_API_URL
        
        if not validate_text(text):
            logger.error("❌ Invalid String send from the client side!")
            return {
                "status": False,
                "message": "AI content check failed, Invalid Text Format",
                "data": None
            }
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
        
        logger.info("📤 Sending request to Watson AI Content API...")
        logger.info(f"➡ URL: {url}")
        logger.info(f"➡ Payload: {payload}")

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, json=payload, headers=headers)
            
         # --------------------------
        # Non-200 response handling
        # --------------------------

        if response.status_code != 200:
            logger.error(
                f"❌ API Error: Status {response.status_code}, Body: {response.text}"
            )
            
            # Save failure log to DB
            new_log = ContentLog(
                status=response.status_code,
                human_score=None,
                readability_score=None,
                credits_used=None,
                credits_remaining=None,
                language=None,
            )
            db.add(new_log)
            await db.commit()

            return {
                "status": False,
                "message": "AI content check failed",
                "data": None
            }

        # --------------------------
        # Successful response
        # --------------------------
        data = response.json()
        
        logger.info("✅ API Success: Watson AI Content API responded successfully")
        logger.info(f"📥 Response: {data}")
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
        logger.exception(f"🔥 Exception occurred during content check: {str(e)}")
        return {
            "status": False,
            "message": str(e),
            "data": None
        }
        
        
async def detect_category(text: str):
    logger.info("🔍 Classifying text category...")
    category = classify_text(text)
    logger.info(f"📌 Classified as: {category}")
    return category