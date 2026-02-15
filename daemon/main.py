from app.server_utils import load_data_from_json, write_data_to_json
from daemon.daemon_utils import get_active_session
from daemon.model import model_response
# from time import sleep
import datetime
import json

## Find active language [OK]: Set when the vocab sent to the backend

## While true [TODO] Find a way to exit the loop

## Call LLM

## Put the modified data into the processed dict and set approved = false


# response = """
# {
#     "staged": {
#         "approved": [
#             {"Word": "hablar", "Article": "", "English": "to speak", "Plural": "", "Grammar": "Verb", "Category": "Motion", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "comer", "Article": "", "English": "to eat", "Plural": "", "Grammar": "Verb", "Category": "Food", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "ir", "Article": "", "English": "to go", "Plural": "", "Grammar": "Verb", "Category": "Motion", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "pensar", "Article": "", "English": "to think", "Plural": "", "Grammar": "Verb", "Category": "Abstract", "Difficulty": "A2", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "gato", "Article": "el", "English": "cat", "Plural": "gatos", "Grammar": "Noun", "Category": "Nature", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "ciudad", "Article": "la", "English": "city", "Plural": "ciudades", "Grammar": "Noun", "Category": "Abstract", "Difficulty": "A2", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "infraestructura", "Article": "la", "English": "infrastructure", "Plural": "", "Grammar": "Noun", "Category": "Abstract", "Difficulty": "B2", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "bonito", "Article": "", "English": "pretty", "Plural": "", "Grammar": "Adjective", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "rojo", "Article": "", "English": "red", "Plural": "", "Grammar": "Adjective", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "interesante", "Article": "", "English": "interesting", "Plural": "", "Grammar": "Adjective", "Category": "Abstract", "Difficulty": "A2", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "rápidamente", "Article": "", "English": "quickly", "Plural": "", "Grammar": "Adverb", "Category": "Motion", "Difficulty": "A2", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "siempre", "Article": "", "English": "always", "Plural": "", "Grammar": "Adverb", "Category": "Time", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "sobre", "Article": "", "English": "on/about", "Plural": "", "Grammar": "Preposition", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
#             {"Word": "contra", "Article": "", "English": "against", "Plural": "", "Grammar": "Preposition", "Category": "Abstract", "Difficulty": "B1", "Count": 0, "SuccessRate": 0.0}
#         ],
#         "disapproved": ["yo", "nosotros", "ellos", "te", "buenos días", "hasta luego", "¿qué tal?", "el", "la", "y", "porque"]
#     }
# }
# """


if __name__ == "__main__":
	# while (True):
	
	## Set the characteristics
	data = load_data_from_json("TEST_PATH")
	language = get_active_session()
	if not data or not data.get(language, None):
		print("No data found in the vocab file, skipping...")
		exit (0)

	vocab = data[language].get('scraped', {}).get('vocabulary', [])

	## Call the LLM 
	response = model_response(vocab, language)
	print(response)
	print(type(response))

	if not response or not response.strip().startswith("{"):
		print("Non-JSON model response, skipping...")
		exit(0)

	## Clean 'scraped' property
	data[language]['scraped']['vocabulary'] = None

	staged = data.setdefault(language, {}).setdefault(
		'staged', {'approved': [], 'disapproved': []})

	new_staged = json.loads(response).get('staged', {})

	approved = staged.setdefault("approved", [])
	existing_words = {w.get("Word") for w in approved}

	## Merge new unique 'staged' property
	for w in new_staged.get("approved", []):
		key = w.get("Word")
		if key not in existing_words:
			approved.append(w)
			existing_words.add(key)

	# Deduplicate disapproved by string value
	disapproved = staged.setdefault("disapproved", [])
	existing_disapproved = set(disapproved)

	for item in new_staged.get("disapproved", []):
		if item not in existing_disapproved:
			disapproved.append(item)
			existing_disapproved.add(item)
	
	## Write data to the JSON file
	write_data_to_json("TEST_PATH", data)

		# sleep(100)
		