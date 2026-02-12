import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.environ["API_KEY"]
try:
	client = genai.Client(api_key=API_KEY)
except ValueError:
	raise ValueError("Error: Invalid API key")

system_prompt = """
	You are a professional lexicographer. 
	Your task is to process a list of words from a non-English language into a clean dictionary.
	Rules:
	1. Remove names, countries, and grammar particles (conjunctions, prepositions).
	2. Lemmatize: Convert verbs to infinitive and nouns to nominative case.
	3. Gender: Identify gender (M, F, N) for nouns.
	4. Difficulty: Categorize words by CEFR level (A1, A2, B1, B2, C1, C2).
	5. Translate: Provide a clear English translation.
	Output ONLY a Markdown table with these columns: Original, Lemma, Type, Gender, Difficulty, English.
	"""

def process_vocabulary(word_list):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Process these words: {', '.join(word_list)}",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1
        )
    )
    return response.text

# Example Usage:
raw_words = ["hablamos", "gato", "Madrid", "bonitas", "el", "comieron"]
dictionary_table = process_vocabulary(raw_words)
print(dictionary_table)
