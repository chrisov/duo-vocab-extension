from app.server_utils import load_data_from_json, write_data_to_json
import argparse

def get_active_session() -> str:
	"""
	Docstring for get_active_session
	
	:return: Description
	:rtype: str
	"""

	session_data = load_data_from_json("SESSION_PATH")
	for language, info in session_data.items():
		if isinstance(info, dict) and info.get("active") is True:
			return language
	return ""



def clear_list_from_json(filepath: str, lang: str, list_name: str):
	data = load_data_from_json(filepath)
	lang_entry = data.setdefault(lang, {})

	if list_name == 'scraped':
		scraped = lang_entry.setdefault('scraped', {})
		scraped['vocabulary'] = []
	elif list_name in ('approved', 'disapproved'):
		staged = lang_entry.setdefault('staged', {})
		staged[list_name] = []
	else:
		raise ValueError(f"Unknown list name to clear: '{list_name}'")

	print(data)
	write_data_to_json(filepath, data)



def process_flags():
	parser = argparse.ArgumentParser(description="Duo Teacher Service")
	parser.add_argument("-t", "--test_mode", action="store_true")
	return parser.parse_args()