
import logging
import os


# ==========================================
# LOCAL LOG DIRECTORY
# ==========================================

LOG_DIR = "/content/logs"

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

LOG_FILE = os.path.join(
    LOG_DIR,
    "system.log"
)


# ==========================================
# LOGGER
# ==========================================

logger = logging.getLogger(
    "DecisionAI"
)

logger.setLevel(logging.INFO)

if logger.hasHandlers():

    logger.handlers.clear()


# ==========================================
# FILE HANDLER
# ==========================================

file_handler = logging.FileHandler(
    LOG_FILE
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(
    formatter
)

logger.addHandler(
    file_handler
)


# ==========================================
# FUNCTIONS
# ==========================================

def log_event(message):

    logger.info(message)


def log_error(message):

    logger.error(message)
