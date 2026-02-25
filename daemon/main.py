from daemon.daemon_utils import get_active_session, process_flags
from daemon.model import model_response, response_example
from daemon.JSONVocab import JSONVocab
from daemon.logger import setup_loggin_config
from app.server_utils import get_path
import argparse
import logging
import json
import time
import os
import signal
import threading

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



def _process_scraped_vocabulary(obj: JSONVocab, test_mode: bool) -> bool:

	## Call the LLM
	if test_mode == False:
		response = model_response(obj.get_scraped_vocab(), obj.get_language())
	else:
		response = response_example

	## Check response's structural validity
	if not response or not response.strip().startswith('{'):
		logger.warning("LLM: Invalid response, skipping...")
		return False

	## Process and persist the new staged vocabulary
	new_staged = json.loads(response).get('staged', {})
	_process_model_response(obj, new_staged)
	return True



def execute_daemon(filepath: str, args: argparse.Namespace, stop_event: threading.Event):
	logger.info("Init SQL engine")

	abs_path = get_path(filepath)
	try:
		last_modific = os.path.getmtime(abs_path)
	except FileNotFoundError:
		logger.warning(f"'{abs_path}': File not found")
		last_modific = 0

	while not stop_event.is_set():
		try:
			current_modific = os.path.getmtime(abs_path)
		except FileNotFoundError:
			logger.warning(f"'{abs_path}': File not found")
			current_modific = 0

		if current_modific > last_modific:
			last_modific = current_modific

			## Process the scraped vocabulary into the 'staged' property
			try:
				obj = JSONVocab(filepath, get_active_session())
				if obj.get_scraped_vocab() != [] and _process_scraped_vocabulary(obj, args.test_mode) == True:
						logger.info(f"'{abs_path}': Processing changes...")
						obj.write_data_to_json()
						logger.info("'scraped' vocabulary processed successfully")
			except Exception as e:
				logger.error(f"Daemon processing: {str(e)}")
		
		# Sleep in small increments so we can respond quickly to shutdown
		for _ in range(int(POLL_INTERVAL * 10)):
			if stop_event.is_set():
				break
			time.sleep(0.1)

	logger.info("Daemon shutting down gracefully")



if __name__ == "__main__":
	args = process_flags()
	logger.debug(f"Test Flag: {args.test_mode}")

	stop_event = threading.Event()

	def _signal_handler(signum, frame):
		logger.info(f"Received signal {signum}; initiating shutdown...")
		stop_event.set()

	# Register handlers for SIGINT and SIGTERM. SIGKILL cannot be caught.
	signal.signal(signal.SIGINT, _signal_handler)
	signal.signal(signal.SIGTERM, _signal_handler)
	# On Windows, optionally handle SIGBREAK
	if hasattr(signal, "SIGBREAK"):
		signal.signal(signal.SIGBREAK, _signal_handler)

	execute_daemon("VOCAB_PATH", args, stop_event)