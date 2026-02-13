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
	You are a professional lexicographer. 
	Your task is to process a list of words from a non-English language into a clean dictionary.
	Every row in the resulted dictionary contains associated information for the corresponding
	word of the input list, in the following format:

	{Word}, {Article}, {English}, {Plural}, {Grammar}, {Category}, {Difficulty}, {Count}, {SuccessRate}

	Rules:
	1. Remove any input word that does not fall under the mentioned grammatical category.
	2. Lemmatize: Convert verbs to infinitive and nouns to nominative case.
	3. Gender: replace adjectives with the masculine gender if not already.
	4. Plural: Provide the plural for nouns. '-' for the other grammar types.
	5. Grammar: Name the grammatical type of the word:
		- Noun
		- Adjective
		- Adverb
		- Preposition
		- Pronoun
		- Phrase
	6. Pronouns: Personal and possessive pronouns are to be removed
	7. Phrases: Only small every-day phrases are kept
	8. Difficulty: Categorize words by CEFR level (A1, A2, B1, B2, C1, C2).
	9. Translate: Provide a clear English translation.
	10. Count: Always equals to 0.
	11. SucceessRate: Always equals to 0.0
	"""

def init():
	return client, system_prompt
