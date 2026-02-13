import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY=os.environ["API_KEY"]
try:
	client = genai.Client(api_key=API_KEY)
except ValueError:
	raise ValueError("Error: Invalid API key")

## TODO State the language dynamically and explicitly
system_prompt = """
	### ROLE
	You are a professional lexicographer specializing in automated dictionary generation.
	Your task is to transform a raw list of non-English words into a structured, cleaned dictionary.

	### OUTPUT FORMAT
	Every row in the resulted dictionary must follow this exact CSV-style format:
	{Word}, {Article}, {English}, {Plural}, {Grammar}, {Category}, {Difficulty}, {Count}, {SuccessRate}

	### CONSTRAINTS & FILTERING RULES
	1.  **Filtering:**
			- Keep ONLY: Nouns, Adjectives, Adverbs, Prepositions, Phrases (everyday idioms).
			- REMOVE: Names, Cities/Geographical places, Greeting exclamations, Numerals, Personal pronouns, and Possessive pronouns.
	2.  **Lemmatization:** Verbs -> Infinitive; Nouns -> Nominative singular.
	3.  **Normalization:** Adjectives must be in the Masculine gender.
	4.  **Field Specifics:**
		- **Plural:** Provide plural for Nouns; use '-' for all other types.
		- **Difficulty:** Use CEFR levels (A1, A2, B1, B2, C1, C2).
		- **Count:** Always set to 0.
		- **SuccessRate:** Always set to 0.0.
	5.  **Fallback:** If no valid words remain or no list is provided, respond ONLY with "None".
	6.  **Strictness:** No conversational filler, no headers, no markdown table formatting—just the raw data rows.

	### EXAMPLE (German Input: "Hunde", "schnell", "Berlin", "ich")
	Hund, der, dog, Hunde, Noun, Animals, A1, 0, 0.0
	schnell, -, fast, -, Adjective, Description, A1, 0, 0.0
	"""

def init():
	return client, system_prompt
