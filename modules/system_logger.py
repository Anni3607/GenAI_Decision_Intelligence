import os
from datetime import datetime

# =====================================================
# LOCAL LOG DIRECTORY
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

# =====================================================
# LOG FILES
# =====================================================

EVENT_LOG_FILE = os.path.join(
    LOG_DIR,
    "events.log"
)

ERROR_LOG_FILE = os.path.join(
    LOG_DIR,
    "errors.log"
)

# =====================================================
# EVENT LOGGER
# =====================================================

def log_event(message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(EVENT_LOG_FILE, "a") as f:

        f.write(
            f"[{timestamp}] EVENT: {message}\n"
        )

# =====================================================
# ERROR LOGGER
# =====================================================

def log_error(message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(ERROR_LOG_FILE, "a") as f:

        f.write(
            f"[{timestamp}] ERROR: {message}\n"
        )
