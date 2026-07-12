import logging
import os
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("weather")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # Always log to console - this works everywhere, including
    # Streamlit Community Cloud where writing files can be restricted.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logger.addHandler(console_handler)

    # Also try to log to a rotating file. This used to crash on a fresh
    # clone / cloud deploy because the "logs/" folder is git-ignored and
    # never got created, so RotatingFileHandler("logs/app.log", ...)
    # raised FileNotFoundError before Streamlit even started rendering.
    try:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
        os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "app.log"), maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        )
        logger.addHandler(file_handler)
    except OSError:
        # Read-only filesystem or similar - console logging above still works.
        logger.warning("File logging unavailable, continuing with console logging only.")
