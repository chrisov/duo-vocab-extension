from .init import init
from google.genai import types
from google.genai.errors import ClientError


## Should it be called once beforethe call
client, system_prompt = init()


# def model_response(word_list: list, lang: str):
#     try:
#         response = client.models.generate_content(
#             model="gemini-2.5-flash-lite",
#             contents=f"Process these words in {lang} language: {', '.join(word_list)}",
#             config=types.GenerateContentConfig(
#                 system_instruction=system_prompt,
#                 temperature=0.1
#             )
#         )
#         return response.text
#     except ClientError as e:
#         if e.code == 429 or getattr(e, "code", None) == 429:
#             return f"Quota exceeded, skipping for now: {str(e.status)}"

# Define the structure of an 'approved' word
word_schema = {
    "type": "OBJECT",
    "properties": {
        "Word": {"type": "STRING"},
        "Article": {"type": "STRING"},
        "English": {"type": "STRING"},
        "Plural": {"type": "STRING"},
        "Grammar": {"type": "STRING"},
        "Category": {"type": "STRING"},
        "Difficulty": {"type": "STRING"},
        "Count": {"type": "INTEGER"},
        "SuccessRate": {"type": "NUMBER"}
    },
    "required": ["Word", "Article", "English", "Plural", "Grammar", "Category", "Difficulty", "Count", "SuccessRate"]
}

# Define the overall response structure
response_schema = {
    "type": "OBJECT",
    "properties": {
        "processed": {
            "type": "OBJECT",
            "properties": {
                "approved": {"type": "ARRAY", "items": word_schema},
                "disapproved": {"type": "ARRAY", "items": {"type": "STRING"}}
            },
            "required": ["approved", "disapproved"]
        }
    },
    "required": ["processed"]
}

def model_response(word_list: list, lang: str):
    try:
        if not word_list:
            return "None"
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=f"Process these words in '{lang}' language: {', '.join(word_list)}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, # Use the prompt from above
                temperature=0,
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        return response.text
    except ClientError as e:
        if e.code == 429 or getattr(e, "code", None) == 429:
            return f"Quota exceeded, skipping for now: {str(e.status)}"
        elif e.code == 503 or getattr(e, "code", None) == 503:
            return f"High demand, try again later: {str(e.status)}"


