from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .schemas import SubmitRequest
from .database import SessionLocal
from .models import AIDetection
from .copyleaks_service import copyleaks_service
from .logger import logger

app = FastAPI(title="AI Content Detection API")


def response(status: bool, msg: str, data=None):
    return JSONResponse({
        "status": status,
        "msg": msg,
        "data": data
    })


@app.post("/api/v1/ai-detect")
def detect_ai(payload: SubmitRequest):
    text = payload.text.strip()

    # 🔥 Validate text length (at least 25 words)
    if len(text.split()) < 25:
        logger.error("Validation failed: less than 25 words.")
        return response(False, "Input text must contain at least 25 words.", None)

    try:
        # Run AI detection
        result = copyleaks_service.detect_ai(text)

        # Save to DB
        db = SessionLocal()
        record = AIDetection(
            scan_id=result["scan_id"],
            ai_score=result["ai_score"],
            human_score=result["human_score"],
            text_length=len(text.split())
        )
        db.add(record)
        db.commit()
        db.close()

        logger.info("AI detection completed successfully.")

        return response(True, "AI detection completed.", {
            "ai_score": result["ai_score"],
            "human_score": result["human_score"],
            "scan_id": result["scan_id"]
        })

    except Exception as e:
        logger.error(f"AI detection error: {str(e)}")
        return response(False, "AI detection failed.", None)
