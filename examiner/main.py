# from dotenv import load_dotenv
# from pathlib import Path
from examiner.examiner_utils import process_staging
from daemon.sql_utils import init_sql
from .logger import setup_loggin_config
import logging
# import os

setup_loggin_config("EXAMINER")
logger = logging.getLogger(__name__)


# PROJECT_DIR = Path(__file__).resolve().parents[1]
# load_dotenv(PROJECT_DIR / "config" / ".env")
# VOCAB_PATH = os.environ["VOCAB_KEY"]
# if not VOCAB_PATH:
# 	logger.warning("VOCAB_KEY missing from env file")
# 	VOCAB_PATH = "VOCAB_PATH"


if __name__ == "__main__":
	conn = init_sql()
	print("Checking for available validation...")
	process_staging(conn)
	conn.close()