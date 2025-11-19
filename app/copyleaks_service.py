import time
from copyleaks.models.submit.ai_detection_document import NaturalLanguageDocument
from copyleaks.copyleaks import Copyleaks

from .token_service import token_service
from .database import SessionLocal
from .models import AIDetection
from .logger import logger


class CopyleaksService:
    def __init__(self):
        pass

    def detect_ai(self, text: str, sandbox: bool = True) -> dict:
        # validate length (Copyleaks requires >= 25 words)
        if len(text.split()) < 25:
            raise ValueError("Text must contain at least 25 words for detection.")

        # get token
        token = token_service.get_valid_token()

        # unique scan id
        scan_id = f"scan-{int(time.time())}"

        # document
        doc = NaturalLanguageDocument(text)
        doc.set_sandbox(sandbox)

        logger.info("Submitting document to Copyleaks...")

        response = Copyleaks.AiDetectionClient.submit_natural_language(
            token, scan_id, doc
        )

        # handle invalid responses
        if not isinstance(response, dict):
            logger.error("Unexpected response type from Copyleaks SDK: %s", type(response))
            raise RuntimeError("Copyleaks detection failed")

        ai_score = float(response["summary"]["ai"]) if response.get("summary") else 0.0
        human_score = float(response["summary"]["human"]) if response.get("summary") else 0.0

        # save results
        self._save_result(scan_id, text, ai_score, human_score)

        logger.info("Detection complete: ai=%s human=%s", ai_score, human_score)

        return {
            "scan_id": scan_id,
            "ai_score": ai_score,
            "human_score": human_score,
            "raw": response,
        }

    def _save_result(self, scan_id, text, ai_score, human_score):
        db = SessionLocal()
        try:
            rec = AIDetection(
                scan_id=scan_id,
                text=text,
                text_length=len(text),
                ai_score=ai_score,
                human_score=human_score,
            )
            db.add(rec)
            db.commit()
        except Exception as e:
            logger.error("Failed to save AI detection result: %s", str(e))
            db.rollback()
            raise
        finally:
            db.close()


# service instance
copyleaks_service = CopyleaksService()
