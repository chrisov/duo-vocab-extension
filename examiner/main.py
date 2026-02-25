from examiner.sql_utils import init_sql, init_staging
from examiner.staging import process_staging
from .logger import setup_loggin_config
from daemon.JSONVocab import JSONVocab
from daemon.daemon_utils import get_active_session
import logging
from sqlite3 import Error

setup_loggin_config("EXAMINER")
logger = logging.getLogger(__name__)


if __name__ == "__main__":
	
	try:
		conn = init_sql()
	except Error as e:
		logger.error(f"Exiting: {str(e)}")
		exit (1)
	
	obj = JSONVocab("VOCAB_PATH", get_active_session())
	logger.info("Checking staging...")
	init_staging(conn, 'staging', obj.get_language(), obj.get_approved())

	approved = obj.get_approved()
	clear_approved = process_staging(conn)
	if clear_approved is not None:
		clear_set = set(clear_approved)
		filtered = [d for d in approved if d['Word'] not in clear_set]

		obj.set_approved(filtered)
		obj.write_data_to_json()
		# obj.set_disapproved(list(set(obj.get_disapproved()) ^ set(clear_approved)))

	logger.info("Back to main menu")

	logger.info(f"Closing connection...")
	print()
	conn.close()
