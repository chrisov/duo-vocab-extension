from daemon.daemon_utils import get_active_session
from daemon.model import model_response
# from time import sleep
import json
from daemon.JSONVocab import JSONVocab

response = """
{
    "staged": {
        "approved": [
            {"Word": "hablar", "Article": "", "English": "to speak", "Plural": "", "Grammar": "Verb", "Category": "Motion", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "comer", "Article": "", "English": "to eat", "Plural": "", "Grammar": "Verb", "Category": "Food", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "ir", "Article": "", "English": "to go", "Plural": "", "Grammar": "Verb", "Category": "Motion", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "pensar", "Article": "", "English": "to think", "Plural": "", "Grammar": "Verb", "Category": "Abstract", "Difficulty": "A2", "Count": 0, "SuccessRate": 0.0},
            {"Word": "gato", "Article": "el", "English": "cat", "Plural": "gatos", "Grammar": "Noun", "Category": "Nature", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "ciudad", "Article": "la", "English": "city", "Plural": "ciudades", "Grammar": "Noun", "Category": "Abstract", "Difficulty": "A2", "Count": 0, "SuccessRate": 0.0},
            {"Word": "infraestructura", "Article": "la", "English": "infrastructure", "Plural": "", "Grammar": "Noun", "Category": "Abstract", "Difficulty": "B2", "Count": 0, "SuccessRate": 0.0},
            {"Word": "bonito", "Article": "", "English": "pretty", "Plural": "", "Grammar": "Adjective", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "rojo", "Article": "", "English": "red", "Plural": "", "Grammar": "Adjective", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "interesante", "Article": "", "English": "interesting", "Plural": "", "Grammar": "Adjective", "Category": "Abstract", "Difficulty": "A2", "Count": 0, "SuccessRate": 0.0},
            {"Word": "rápidamente", "Article": "", "English": "quickly", "Plural": "", "Grammar": "Adverb", "Category": "Motion", "Difficulty": "A2", "Count": 0, "SuccessRate": 0.0},
            {"Word": "siempre", "Article": "", "English": "always", "Plural": "", "Grammar": "Adverb", "Category": "Time", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "sobre", "Article": "", "English": "on/about", "Plural": "", "Grammar": "Preposition", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "contra", "Article": "", "English": "against", "Plural": "", "Grammar": "Preposition", "Category": "Abstract", "Difficulty": "B1", "Count": 0, "SuccessRate": 0.0}
        ],
        "disapproved": ["yo", "nosotros", "ellos", "te", "buenos días", "hasta luego", "¿qué tal?", "el", "la", "y", "porque"]
    }
}
"""


def	process_vocab(obj: JSONVocab):

	## Set the characteristics
	# data = load_data_from_json('TEST_PATH')
	# language = get_active_session()

	if not obj.get_data() or not obj.get_data().get(obj.get_language(), None):
		print('No data found in the vocab file, skipping...')
		return

	## Call the LLM 
	# response = model_response(obj.get_scraped_vocab(), obj.get_language())

	# print(response)
	# print(type(response))

	if not response or not response.strip().startswith('{'):
		print('Non-JSON model response, skipping...')
		return

	## Clean 'scraped' property
	# data[language]['scraped']['vocabulary'] = None
	obj.set_scraped_vocab([])

	# staged = data.setdefault(language, {}).setdefault(
	# 	'staged', {'approved': [], 'disapproved': []})

	## Merge new unique 'staged' property (approved)
	new_staged = json.loads(response).get('staged', {})
	# approved = staged.setdefault('approved', [])

	if not obj.get_staged():
		obj.set_staged({})

	# existing_words = {w.get('Word') for w in approved}
	approved = obj.get_approved() or []
	existing_words = {w.get('Word') for w in approved}

	for w in new_staged.get('approved', []):
		key = w.get('Word')
		if key not in existing_words:
			approved.append(w)
			existing_words.add(key)
	obj.set_approved(approved)

	## Merge new unique 'staged' property (disapproved)
	# existing_disapproved = set(disapproved)
	disapproved = obj.get_disapproved() or []
	existing_disapproved = set(disapproved)

	for item in new_staged.get('disapproved', []):
		if item not in existing_disapproved:
			disapproved.append(item)
			existing_disapproved.add(item)
	obj.set_disapproved(disapproved)
	
	## Write data to the JSON file
	obj.write_data_to_json()

		# sleep(100)



if __name__ == "__main__":
	obj = JSONVocab("VOCAB_PATH", get_active_session())
	process_vocab(obj)
