from app.server_utils import load_data_from_json, write_data_to_json
from copy import deepcopy
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
		self.__data = load_data_from_json(filepath)
		self.__filepath = filepath
		self.__language = language

		# Ensure language entry exists in the JSON structure
		if self.__language not in self.__data:
			self.__data[self.__language] = {}

		lang_data = self.__data[self.__language]

		# Initialize scraped/staged sections if missing
		self.__scraped = lang_data.get('scraped')
		if self.__scraped is None:
			self.__scraped = {"timestamp": str(datetime.now()), "vocabulary": []}
			lang_data['scraped'] = self.__scraped

		self.__staged = lang_data.get('staged')
		if self.__staged is None:
			self.__staged = {}
			lang_data['staged'] = self.__staged


	# def __del__(self):
		# [TODO] Execute Query to the staging {lang} table
		# write_data_to_json(self.__filepath, self.__data)


	def get_filepath(self) -> str:
		return (self.__filepath)

	def get_data(self) -> dict:
		return self.__data

	def get_language(self) -> str:
		return self.__language

	def get_approved(self) -> dict:
		return self.__staged.get('approved', [])

	def get_staged(self) -> dict:
		return self.__staged

	def get_disapproved(self) -> dict:
		return self.__staged.get('disapproved', [])

	def get_scraped_vocab(self) -> list:
		return self.__scraped.get('vocabulary', [])


	def init_scraped(self):
		self.__scraped.setdefault('timestamp', str(datetime.now()))
		self.__scraped.setdefault('vocabulary', [])
		self.__data.setdefault(self.__language, {})['scraped'] = self.__scraped


	def init_staged(self):
		self.__staged.setdefault('timestamp', str(datetime.now()))
		self.__staged.setdefault('approved', [])
		self.__staged.setdefault('disapproved', [])
		self.__data.setdefault(self.__language, {})['staged'] = self.__staged


	def set_scraped_vocab(self, new_vocab: list):
		if self.__scraped is None:
			self.init_scraped()
		self.__scraped['vocabulary'] = deepcopy(new_vocab)


	def set_approved(self, new_appr: list):
		if self.__staged is None:
			self.init_staged()
		self.__staged['approved'] = deepcopy(new_appr)


	def set_disapproved(self, new_disappr: list):
		if self.__staged is None:
			self.init_staged()
		self.__staged['disapproved'] = list(new_disappr)
	

	def set_staged_timestamp(self):
		self.__staged['timestamp'] = str(datetime.now())

	def write_data_to_json(self):
		write_data_to_json(self.__filepath, self.__data)


	def __repr__(self):
		return(
			f"\nLanguage: '{self.__language}'\n"
			f"Unprocessed vocab: '{self.__scraped}'\n"
			f"Processed vocab: '{self.__staged}'\n"
		)


if __name__ == "__main__":
	obj = JSONVocab("TEST_PATH", 'pt')
	print(obj)
