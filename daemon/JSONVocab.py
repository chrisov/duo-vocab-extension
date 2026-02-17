from app.server_utils import load_data_from_json, write_data_to_json
from copy import deepcopy

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
		self.__scraped = (self.__data).get(language).get('scraped')
		self.__staged = (self.__data).get(language).get('staged')


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


	def get_approved(self) -> dict:
		return self.__staged.get('approved', {})

	def get_staged(self) -> dict:
		return self.__staged


	def get_disapproved(self) -> dict:
		return self.__staged.get('disapproved', {})


	def get_scraped_vocab(self) -> list:
		return self.__scraped.get('vocabulary', [])


	def set_staged(self, new_dict: dict):
		if self.__staged is None:
			self.__staged = {}
			self.__data.setdefault(self.__language, {})['staged'] = self.__staged
		self.__staged = deepcopy(new_dict)

	def set_scraped_vocab(self, new_vocab: list):
		if self.__scraped is None:
			self.__scraped = {}
			self.__data.setdefault(self.__language, {})['scraped'] = self.__scraped
		self.__scraped['vocabulary'] = deepcopy(new_vocab)


	def set_approved(self, newdict: list):
		if self.__staged is None:
			self.__staged = {}
			self.__data.setdefault(self.__language, {})['staged'] = self.__staged
		self.__staged['approved'] = deepcopy(newdict)


	def set_disapproved(self, newlist: list):
		if self.__staged is None:
			self.__staged = {}
			self.__data.setdefault(self.__language, {})['staged'] = self.__staged
		self.__staged['disapproved'] = list(newlist)
	

	def write_data_to_json(self):
		write_data_to_json(self.__filepath, self.__data)


	def __repr__(self):
		return(
			f"\nLanguage: '{self.__language}'\n"
			f"Unprocessed vocab: '{self.__scraped}'\n"
			f"Processed vocab: '{self.__staged}'\n"
		)


if __name__ == "__main__":
	obj = JSONVocab("VOCAB_COPY_PATH", 'pt')
	print(obj)
