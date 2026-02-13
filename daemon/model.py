from .init import init
from google.genai import types


client, system_prompt = init()


def model_response(word_list):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Process these words: {', '.join(word_list)}",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1
        )
    )
    return response.text

