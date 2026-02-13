from .init import init
from google.genai import types
from google.genai.errors import ClientError


## Should it be called once beforethe call
client, system_prompt = init()


def model_response(word_list: list, lang: str):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Process these words in {lang} language: {', '.join(word_list)}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.1
            )
        )
        return response.text
    except ClientError as e:
        # 429 quota exceeded
        if e.code == 429 or getattr(e, "code", None) == 429:
            return f"Quota exceeded, skipping for now: {str(e.status)}"

