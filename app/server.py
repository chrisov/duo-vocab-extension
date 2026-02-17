import os
from flask import Flask
from flask_cors import CORS
from app.server_utils import load_data_from_json, write_data_to_json, parse_request, set_active_session


app = Flask(__name__)
CORS(app)
VOCAB_KEY = os.getenv("VOCAB_KEY")


def _handle_save_vocab(language: str, entry: dict, vocab_key: str | None = None) -> tuple:
    ## Loads existing session data or creates new
    key = vocab_key or VOCAB_KEY
    vocab_data = load_data_from_json(key)

    ## Updates the scraped vocabulary
    if language not in vocab_data or not (
        vocab_data.get(language, {}).get('scraped', {}).get('vocabulary', [])
        ):
        vocab_data[language] = {'scraped': entry}
    else:
        localVocab = set()
        localVocab.update(vocab_data[language]['scraped']['vocabulary'])
        localVocab.update(entry['vocabulary'])
        vocab_data[language]['scraped']['timestamp'] = entry['timestamp']
        vocab_data[language]['scraped']['vocabulary'] = list(localVocab)

    write_data_to_json(key, vocab_data)

    return "Vocab sent succesfully", 200



@app.route('/save-vocab', methods=['POST'])
def save_vocab() -> tuple:
    """
    Saves extracted vocab to a JSON file.

    :return: The response and its status code.
    :rtype: tuple
    """

    ## Accepts language data from server
    try:
        language, entry = parse_request(['language', 'timestamp', 'vocabulary'])
    except ValueError as e:
        return f"Error: {str(e)}", 400
    
    return _handle_save_vocab(language, entry)


@app.route('/save-session', methods=['POST'])
def save_session() -> tuple:
    """
    Saves the last session's details on a JSON file.

    :return: The response and its status code.
    :rtype: tuple
    """

    ## Loads existing session data or creates new
    session_data = load_data_from_json("SESSION_PATH")

    ## Accepts language data from server
    try:
        language, entry = parse_request(['language', 'timestamp', 'active'],
                                        ['CurrentSection', 'CurrentUnit'])
    except ValueError as e:
        return f"Error: {str(e)}", 400

    ## Update new entry
    session_data[language] = entry

    ## Marking other languages as inactive
    set_active_session(session_data, language)

    # Write everything back to the JSON file
    write_data_to_json("SESSION_PATH", session_data)

    return "Session sent successfully", 200



if __name__ == '__main__':
    app.run(port=5000)