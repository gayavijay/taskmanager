# config.py
import os
import logging

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Now safe to configure logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

DATABASE_URL = "sqlite:///tasks.db"
