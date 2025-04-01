import os
import logging
from datetime import datetime

# Create a dedicated logger
logger = logging.getLogger("CustomLogger")
logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Create a stream handler (console output, warnings and above)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# Create a file handler (file output, all messages)
timestamp = datetime.now().strftime("%y%m%d_%H%M")
log_path = os.path.join(os.getcwd(), "logs", f"clatr_log_{timestamp}.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Attach both handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
