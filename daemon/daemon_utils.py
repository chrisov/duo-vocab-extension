import time
from app.server_utils import load_data_from_json


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
		