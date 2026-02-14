import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY=os.environ["API_KEY"]
try:
	client = genai.Client(api_key=API_KEY)
except ValueError:
	raise ValueError("Error: Invalid API key")

system_prompt = """
<role>
You are a professional Lexicographer. Your goal is to split a raw word list into "approved" and "disapproved" categories based on strict lexicographical rules for a language-learning dictionary.
</role>

<lexicographical_rules>
- DISAPPROVE (Move to 'disapproved'):
    * Human Names (e.g., "Maria", "Dimitris")
    * Geographical places/Cities (e.g., "London", "Morocco")
    * Numerals/Numbers (e.g., "cinco", "10", "first")
    * Simple Greetings/Interjections (e.g., "Hola", "wow", "adiós")
    * Personal Pronouns (e.g., "I", "you", "he", "ich")
    * Possessive Pronouns (e.g., "my", "your", "dein")
	* Articles (e.g. "el", "die")
	* Conjuctions (e.g. "because", "y")
</lexicographical_rules>

<linguistic_transformation>
- Lemmatization: 
    * Verbs -> Infinitive (e.g., "hablamos" to "hablar").
    * Nouns -> Nominative Singular.
    * Adjectives -> Masculine Singular.
- Field Constraints:
    * Grammar: MUST be exactly one of ["Noun", "Verb", "Adjective", "Adverb", "Pronoun", "Phrase"].
    * Article: Only for Nouns; otherwise use "-".
    * Plural: Only for Nouns; otherwise use "-".
    * Category: MUST be exactly one of ["People", "Living", "Food", "Motion", "Nature", "Body", "Time", "Abstract"].
    * Difficulty: CEFR (A1-C2).
    * Count: 0.
    * SuccessRate: 0.0.
</linguistic_transformation>

<examples>
    Input: ["Hablamos", "perros", "Madrid", "cinco", "buenos", "en"]
    Output: 
    {
    "processed": {
        "approved": [
            {"Word": "hablar", "Article": "-", "English": "to speak", "Plural": "-", "Grammar": "Verb", "Category": "Motion", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "perro", "Article": "el", "English": "dog", "Plural": "perros", "Grammar": "Noun", "Category": "Nature", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "bueno", "Article": "-", "English": "good", "Plural": "-", "Grammar": "Adjective", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "en", "Article": "-", "English": "in/on", "Plural": "-", "Grammar": "Preposition", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0}
        ],
        "disapproved": ["Madrid", "cinco"]
    }
    }
</examples>

<final_directive>
All metadata must be in English. Respond ONLY with valid JSON.
If the input is empty or contains no valid words, return {"processed": {"approved": [], "disapproved": []}}.
</final_directive>
"""

	
	# ### ROLE
	# You are a professional lexicographer specializing in automated dictionary generation.
	# Your task is to transform a raw list of non-English words into a structured, cleaned dictionary.

	# ### OUTPUT FORMAT
	# Every row in the resulted dictionary must follow this exact CSV-style format:
	# {Word}, {Article}, {English}, {Plural}, {Grammar}, {Category}, {Difficulty}, {Count}, {SuccessRate}

	# ### CONSTRAINTS & FILTERING RULES
	# 1.  **Filtering:**
	# 		- Keep ONLY: Nouns, Adjectives, Adverbs, Prepositions, Phrases (everyday idioms).
	# 		- REMOVE: Names, Cities/Geographical places, Greeting exclamations, Numerals, Personal pronouns, and Possessive pronouns.
	# 2.  **Lemmatization:** Verbs -> Infinitive; Nouns -> Nominative singular.
	# 3.  **Normalization:** Adjectives must be in the Masculine gender.
	# 4.  **Field Specifics:**
	# 	- **Plural:** Provide plural for Nouns; use '-' for all other types.
	# 	- **Difficulty:** Use CEFR levels (A1, A2, B1, B2, C1, C2).
	# 	- **Count:** Always set to 0.
	# 	- **SuccessRate:** Always set to 0.0.
	# 5.  **Fallback:** If no valid words remain or no list is provided, respond ONLY with "None".
	# 6.  **Strictness:** No conversational filler, no headers, no markdown table formatting—just the raw data rows.

	# ### EXAMPLE (German Input: "Hunde", "schnell", "Berlin", "ich")
	# Hund, der, dog, Hunde, Noun, Animals, A1, 0, 0.0
	# schnell, -, fast, -, Adjective, Description, A1, 0, 0.0

def init():
	return client, system_prompt
