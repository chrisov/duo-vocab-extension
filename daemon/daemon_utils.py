import time
from app.server_utils import load_data_from_json, write_data_to_json


def timing_function(func):
	"""
	Timer decorator function
	
	:param func: Function to be decorated
	"""

	def wrapper():
		start = time.perf_counter
		func()
		end = time.perf_counter
		print(f"'{func}' execution time: {'{:.2e}'.format(end - start)}")
	return wrapper



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
