import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

logger = logging.getLogger("AI-Content")
logger.setLevel(logging.INFO)

# -----------------------------
# Console Handler
# -----------------------------
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(console_formatter)

# -----------------------------
# File Handler (Rotating)
# -----------------------------
file_handler = RotatingFileHandler(
    LOG_FILE_PATH,
    maxBytes=5 * 1024 * 1024,  # 5 MB per file
    backupCount=5              # keep last 5 logs
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)

# Attach handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
