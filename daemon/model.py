from .init import init
from google.genai import types
from google.genai.errors import ClientError, ServerError
import logging


logger = logging.getLogger(__name__)

## Should it be called once beforethe call
client, system_prompt = init()


## Define the structure of an 'approved' word
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


## Define the overall response structure
response_schema = {
    "type": "OBJECT",
    "properties": {
        "staged": {
            "type": "OBJECT",
            "properties": {
                "approved": {"type": "ARRAY", "items": word_schema},
                "disapproved": {"type": "ARRAY", "items": {"type": "STRING"}}
            },
            "required": ["approved", "disapproved"]
        }
    },
    "required": ["staged"]
}

## Response example for testing purposes
response_example = """
{
    "staged": {
    "timestamp": "2025-01-01T00:00:00Z",
        "approved": [
            {"Word": "falar", "Article": "", "English": "to speak", "Plural": "", "Grammar": "Verb", "Category": "Motion", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "ir", "Article": "", "English": "to go", "Plural": "", "Grammar": "Verb", "Category": "Motion", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "gato", "Article": "o", "English": "cat", "Plural": "gatos", "Grammar": "Noun", "Category": "Nature", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "bonito", "Article": "", "English": "pretty", "Plural": "", "Grammar": "Adjective", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "vermelho", "Article": "", "English": "red", "Plural": "", "Grammar": "Adjective", "Category": "Abstract", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0},
            {"Word": "rapidamente", "Article": "", "English": "quickly", "Plural": "", "Grammar": "Adverb", "Category": "Motion", "Difficulty": "A2", "Count": 0, "SuccessRate": 0.0},
            {"Word": "sempre", "Article": "", "English": "always", "Plural": "", "Grammar": "Adverb", "Category": "Time", "Difficulty": "A1", "Count": 0, "SuccessRate": 0.0}
        ],
        "disapproved": ["eu", "bom dia", "até logo", "tudo bem?", "o", "a", "e"]
    }
}
"""

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
    except (ClientError, ServerError) as e:
        if getattr(e, "code", None) in (429, ):
            logger.error(f"Quota exceeded, skipping for now: {str(e.status)}")
            return None
        elif getattr(e, "code", None) in (503, ):
            logger.error(f"High demand, try again later: {str(e.status)}")
            return None


