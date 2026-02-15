from app.server_utils import load_data_from_json, write_data_to_json
from datetime import datetime

## "pt": {
## 	"scraped": {
## 		"timestamp": str,
## 		"vocabulary": []
## 	},
## 	"staged": {
## 		"timestamp": str,
## 		"approved": [{}],
## 		"disapproved": []
## 	}
## }

class JSONVocab:

	def __init__(self, filepath, language: str | None = None):
		self.__filepath = filepath
		self.__data = load_data_from_json(filepath)
		self.__language = language
		self.__scraped = ((self.__data).get(language)).get('scraped')
		self.__staged = ((self.__data).get(language)).get('staged')
		self.__last_process_time = datetime.datetime.now()


	def __del__(self):
		print("Deconstructor")
		# [TODO] Execute Query to the staging {lang} table
		# write_data_to_json(self.__filepath, self.__data)


	def get_filepath(self) -> str:
		return (self.__filepath)


	def get_data(self) -> dict:
		return self.__data


	def get_language(self) -> str:
		return self.__language


	def get_unporcessed(self) -> dict:
		return self.__unprocessed


	def get_processed(self) -> dict:
		return self.__processed


	# def check_timestamp(self):
	# [TODO] DEEP COPY A LIST OF DICTS
	def set_approved(self, newdict: list):
		self.__processed.get('approved', {}) = newdict.copy()


	def set_disapproved(self, newdict: dict):
		self.__processed.get('disapproved', {}) = newdict.copy()


	def __repr__(self):
		return(
			f"\nLanguage: '{self.__language}'\n"
			f"Unprocessed vocab: '{self.__unprocessed}'\n"
			f"Processed vocab: '{self.__processed}'\n"
		)


if __name__ == "__main__":
	obj = JSONVocab("VOCAB_COPY_PATH", 'pt')
	print(obj)
