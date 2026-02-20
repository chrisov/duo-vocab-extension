from daemon.daemon_utils import get_active_session
from daemon.model import model_response, response_example
from daemon.JSONVocab import JSONVocab
from daemon.staging import staging
from daemon.sql_utils import init_sql
from daemon.logger import setup_loggin_config
from app.server_utils import get_path
import logging
import json
import time
import os

setup_loggin_config("DAEMON")
logger = logging.getLogger(__name__) 
logger.info("Service started and ready")

POLL_INTERVAL = 15.0

def	_process_model_response(obj: JSONVocab, new_dict: dict):
	"""
	Merges the newly generated vocabulary with the old one
	
	:param obj: Already existing JSON object
	:type obj: JSONVocab
	:param new_dict: New vocabulary
	:type new_dict: dict
	"""

	## Creates an empty 'scraped' property if not existing
	if not obj.get_data():
		obj.init_scraped()

	## Creates an empty 'staged' property if not existing
	if not obj.get_staged():
		obj.init_staged()

	## Gets the 'approved' property in the old vocab
	approved = obj.get_approved() or []
	existing_words = {w.get('Word') for w in approved}

	## Updates the timestamp
	obj.set_staged_timestamp()

	## Merges new unique 'approved' with the old property
	for w in new_dict.get('approved', []):
		key = w.get('Word')
		if key not in existing_words:
			approved.append(w)
			existing_words.add(key)
	obj.set_approved(approved)

	## Gets the 'disapproved' property in the old vocab
	disapproved = obj.get_disapproved() or []
	existing_disapproved = set(disapproved)

	## Merges new unique 'disapproved' with the old property
	for item in new_dict.get('disapproved', []):
		if item not in existing_disapproved:
			disapproved.append(item)
			existing_disapproved.add(item)
	obj.set_disapproved(disapproved)

	## Clears the 'scraped' vocabulary
	obj.set_scraped_vocab([])



def process_scraped_vocabulary(obj: JSONVocab, test_mode: bool = False):

	## Call the LLM
	if test_mode == False:
		response = model_response(obj.get_scraped_vocab(), obj.get_language())
	else:
		response = response_example

	## Check response's structural validity
	if not response or not response.strip().startswith('{'):
		logger.warning("LLM: Invalid response, skipping")
		return

	## Process and persist the new staged vocabulary
	new_staged = json.loads(response).get('staged', {})
	_process_model_response(obj, new_staged)



def execute_daemon(filepath: str):
	logger.info("Init SQL engine")
	conn = init_sql()

	abs_path = get_path(filepath)
	try:
		last_modific = os.path.getmtime(abs_path)
	except FileNotFoundError:
		logger.warning(f"'{abs_path}': File not found")
		last_modific = 0

	try:
		while True:
			try:
				current_modific = os.path.getmtime(abs_path)
			except FileNotFoundError:
				logger.warning(f"'{abs_path}': File not found")
				current_modific = 0

			if current_modific > last_modific:
				logger.info(f"'{abs_path}': Processing changes...")
				last_modific = current_modific

				## Process the scraped vocabulary into the 'staged' property
				try:
					obj = JSONVocab(filepath, get_active_session())
					if obj.get_scraped_vocab() != []:
						process_scraped_vocabulary(obj)
						obj.write_data_to_json()
						logger.info("Processed 'scraped' vocabulary")
						staging(conn, obj)
				except Exception as e:
					logger.error(f"Daemon processing: {str(e)}")
			time.sleep(POLL_INTERVAL)
	finally:
		logger.info("Disconnecting from DB...")
		conn.close()

if __name__ == "__main__":
	execute_daemon("VOCAB_PATH")