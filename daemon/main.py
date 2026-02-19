from daemon.daemon_utils import get_active_session
from daemon.model import model_response, response_example
from daemon.JSONVocab import JSONVocab
import json


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



def handle_daemon(test_mode: bool = False):

	## Load vocab for the currently active session
	obj = JSONVocab("VOCAB_PATH", get_active_session())

	## Call the LLM
	if test_mode == False:
		response = model_response(obj.get_scraped_vocab(), obj.get_language())
	else:
		response = response_example
	if not response or not response.strip().startswith('{'):
		print('Non-JSON model response, skipping...')
		return

	## Process and persist the new staged vocabulary
	new_staged = json.loads(response).get('staged', {})
	_process_model_response(obj, new_staged)
	obj.write_data_to_json()


if __name__ == "__main__":
	handle_daemon(test_mode=True)	
