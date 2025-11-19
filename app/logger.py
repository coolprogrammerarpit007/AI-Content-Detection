import logging
from logging.handlers import RotatingFileHandler
import os


LOG_DIR = os.path.join(os.getcwd(), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)


logger = logging.getLogger("ai_detection_api")
logger.setLevel(logging.INFO)


handler = RotatingFileHandler(os.path.join(LOG_DIR, "app.log"), maxBytes=5_000_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# Also stream to console for dev
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)