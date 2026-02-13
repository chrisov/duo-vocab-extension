import json
from pathlib import Path
from flask import request


# Resolve paths relative to the project root (one level above this file's directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
PATHS_FILE = CONFIG_DIR / "paths.json"


def safe_path_check(filepath: str) -> str:
	"""
	Loads the paths.json safely, checks and returns the requested JSON filepath.
		
	:param filepath: The requested JSON file.
	:type filepath: str

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

	## Retrieves the filepath from the 
	try:
		data_path = Path(paths[filepath])
	except KeyError as e:
		raise KeyError(f"'{filepath}' does not exist in paths.json") from e
	return data_path



def load_data_from_json(filepath: str) -> dict:
	"""Loads JSON data for the given filepath using paths.json as a lookup.
	
	:param filepath: The JSON file to look for in the paths.json.
	:type filepath: str

	:return: The requested contents of the JSON file.
	:rtype: dict
	"""

	## Loads the filepath
	data_path = safe_path_check(filepath)

	## Creates and init the requested file if not existing
	if data_path.suffix == ".json":
		data_path.parent.mkdir(parents=True, exist_ok=True)
		if not data_path.exists():
			print(f"'{data_path}': Non existing file, created on the spot.")
			data_path.write_text("{}", encoding="utf-8")

	## Returns the contents of the requested file
	if data_path.is_file():
		try:
			return json.loads(data_path.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			print(f"'{data_path}': Invalid format, return an empty dict instead.")
			data_path.write_text("{}", encoding="utf-8")
	return {}



def write_data_to_json(filepath: str, data: dict):
	"""
	Writes data into a JSON file, using the paths.json as lookup.
	
	:param filepath: The requested JSON file.
	:type filepath: str
	:param data: The data to be written.
	:type data: dict
	"""

	## Loads the filepath
	data_path = safe_path_check(filepath)

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
	dict = load_data_from_json("VOCAB_PATH")
	print(f"VOCAB_PATH:\n{dict}'\n")
	dict = load_data_from_json("BACKEND_URL")
	print(f"BACKEND_URL:\n{dict}'\n")
	dict = load_data_from_json("SESSION_PATH")
	print(f"SESSION_PATH:\n{dict}'\n")