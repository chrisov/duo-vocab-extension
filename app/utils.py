import json
from pathlib import Path
from flask import request


CONFIG_DIR = Path("../config")
PATHS_FILE = CONFIG_DIR / "paths.json"


def safe_path_check(key: str) -> str:
	"""
	Loads the paths.json safely, checks and returns the requested JSON file.
		
	:param key: The requested JSON file.
	:type key: str

	:return: The path to the requested JSON file.
	:rtype: str
	"""

	## Creates the config dir if not existing
	CONFIG_DIR.mkdir(parents=True, exist_ok=True)
	if not PATHS_FILE.exists():
		PATHS_FILE.write_text("{}", encoding="utf-8")

	## Loads the paths.json
	try:
		paths = json.loads(PATHS_FILE.read_text(encoding="utf-8"))
	except json.JSONDecodeError as e:
		raise ValueError("paths.json is empty or contains invalid JSON") from e

	## Retrieves the key from the 
	try:
		data_path = Path(paths[key])
	except KeyError as e:
		raise KeyError(f"'{key}' does not exist in paths.json") from e
	return data_path



def safe_load_data(key: str) -> dict:
	"""Loads JSON data for the given key using paths.json as a lookup.
	
	:param key: The JSON file to look for in the paths.json.
	:type key: str

	:return: The requested contents of the JSON file.
	:rtype: dict
	"""

	## Loads the filepath
	data_path = safe_path_check(key)

	## Returns the contents of the requested file
	if data_path.is_file():
		try:
			return json.loads(data_path.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			print(f"'{data_path}': Invalid format, return an empty dict instead.")
			return {}
	else:
		print(f"'{data_path}': Not a valid json file, return an empty dict instead.")
		return {}



def safe_write_data(key: str, data: dict):
	"""
	Writes data into a JSON file, using the paths.json as lookup.
	
	:param key: The requested JSON file.
	:type key: str
	:param data: The data to be written.
	:type data: dict
	"""

	## Loads the filepath
	data_path = safe_path_check(key)

	## Writes to the file
	with open(data_path, "w", encoding='utf-8') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)
   


def parse_request(required: list[str], optional: list[str] | None = None) -> tuple:
	"""
	Requests specified data from server.

	:param required: The requested fields: The first element of the list is required.
	:type fields: list[str]
	:param optional: Optional requested fields. None by default
	:type kwrgs: list[str]
	:return: A tuple of the requested data.
	:rtype: tuple
	"""


	data = request.get_json(silent=True)
	if not data:
		raise ValueError("Missing JSON body")

	language = data.get(required[0])
	fields = {}

	## Parse required fields
	for req in required[1:]:
		if req not in data:
			raise ValueError(f"Required key missing: {req}")
		fields[req] = data.get(req)

	## Parse optional fields
	if optional is not None:
		for opt in optional:
			if opt in data:
				fields[opt] = data.get(opt)

	return language, fields



if __name__ == "__main__":
	dict = safe_load_data("SESSION_PATH")
	print(dict)