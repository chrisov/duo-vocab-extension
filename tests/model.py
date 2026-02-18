from app.server_utils import load_data_from_json, write_data_to_json
from app.model.utils import str_to_list

# Example Usage:
raw_words = [
    # Verbs in different forms (test lemmatization)
    "hablamos",       # hablar (1pl pres)
    "comieron",       # comer (3pl past)
    "fui",            # ir/ser (irregular)
    "pensando",       # pensar (gerund)

    # Nouns (singular/plural + simple vs more advanced)
    "gato",
    "gatos",
    "ciudad",
    "ciudades",
    "infraestructura",   # more advanced noun

    # Adjectives (different gender/number → should end up masculine singular)
    "bonitas",
    "rojos",
    "interesantes",

    # Adverbs
    "rápidamente",
    "siempre",

    # Prepositions
    "sobre",
    "contra",

    # Pronouns
    "yo",
    "nosotros",
    "ellos",
    "te",

    # Everyday phrases (should be kept as phrases)
    "buenos días",
    "hasta luego",
    "¿qué tal?",

    # Things that should likely be removed (not in allowed grammar categories)
    "el",             # article
    "la",
    "y",              # conjunction
    "porque",         # conjunction
    "123",            # number
    "!!!"             # punctuation
]

model_output = """
gato, el, cat, gatos, Noun, -, A1, 0, 0.0
ciudad, la, city, ciudades, Noun, -, A1, 0, 0.0
infraestructura, la, infrastructure, infraestructuras, Noun, -, B2, 0, 0.0
bonito, -, beautiful, -, Adjective, -, A1, 0, 0.0
rojo, -, red, -, Adjective, -, A1, 0, 0.0
interesante, -, interesting, -, Adjective, -, A2, 0, 0.0
rápidamente, -, quickly, -, Adverb, -, B1, 0, 0.0
siempre, -, always, -, Adverb, -, A1, 0, 0.0
sobre, -, on; about, -, Preposition, -, A1, 0, 0.0
contra, -, against, -, Preposition, -, A2, 0, 0.0
buenos días, -, good morning, -, Phrase, -, A1, 0, 0.0
hasta luego, -, see you later, -, Phrase, -, A1, 0, 0.0
¿qué tal?, -, How are you?, -, Phrase, -, A1, 0, 0.0
"""

if __name__ == "__main__":
	print("\nLoading JSON vocabulary file...\n")
	vocab_data = load_data_from_json("VOCAB_COPY_PATH")
	print(vocab_data)

	# print("Loading model response...\n\n")
	# dictionary_table = model_response(raw_words)
	# print(dictionary_table)

	print("\nPrinting resulted table...")
	list = str_to_list(model_output)
	for i, row in enumerate(list):
		print(f"{i}:", end=' ')
		for col in row:
			print(f"{col}", end='\t')
		print()

	print("Merging data...")
	vocab_data['pt']['vocabulary'] = list
	print(vocab_data)

	print("\nWriting data to the JSON...")
	write_data_to_json("VOCAB_COPY_PATH", vocab_data)
	

	
