import os
import socket
import sys
from flask import Flask
from flask_cors import CORS
from app.logger import setup_loggin_config
from app.server_utils import load_data_from_json, write_data_to_json, parse_request, set_active_session, get_path
import logging
from pathlib import Path
from dotenv import load_dotenv


## Setup 'Web' logger
setup_loggin_config("WEB")
logger = logging.getLogger(__name__)

# Silence Flask/Werkzeug default HTTP access logging
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logger.info("Service started and ready")

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
if not load_dotenv(CONFIG_DIR / ".env"):
    logger.warning(f"Could not load .env from '{CONFIG_DIR}'")
VOCAB_KEY = os.getenv("VOCAB_KEY")
if not VOCAB_KEY:
    logger.error(f"{VOCAB_KEY}: Missing from .env file")
    VOCAB_KEY = "VOCAB_PATH"

app = Flask(__name__)
CORS(app)


def _handle_save_vocab(language: str, entry: dict, vocab_key: str | None = None) -> tuple:
    ## Loads existing session data or creates new
    key = vocab_key or VOCAB_KEY
    vocab_data = load_data_from_json(key)
    lang_data = vocab_data.get(language, {})

    ## Updates the scraped vocabulary
    if not lang_data.get('scraped', {}).get('vocabulary'):
        lang_data['scraped'] = entry
        vocab_data[language] = lang_data
    else:
        lang_data['scraped']['timestamp'] = entry['timestamp']
        localVocab = set()
        localVocab.update(lang_data['scraped']['vocabulary'])
        localVocab.update(entry['vocabulary'])
        lang_data['scraped']['vocabulary'] = list(localVocab)
        vocab_data[language] = lang_data

    write_data_to_json(key, vocab_data)

    logger.info("Vocabulary extracted successfully")

    return "Vocab sent succesfully", 200



@app.route('/save-vocab', methods=['POST'])
def save_vocab() -> tuple:
    """
    Saves extracted vocab to a JSON file.

    :return: The response and its status code.
    :rtype: tuple
    """

    logger.info("Extracting vocabulary...")

    ## Accepts language data from server
    try:
        language, entry = parse_request(['language', 'timestamp', 'vocabulary'])
    except ValueError as e:
        logger.error(f"Error extracting vocabulary: {str(e)}")
        return f"Error: {str(e)}", 400
    
    return _handle_save_vocab(language, entry)



@app.route('/save-session', methods=['POST'])
def save_session() -> tuple:
    """
    Saves the last session's details on a JSON file.

    :return: The response and its status code.
    :rtype: tuple
    """

    logger.info("Updating session info...")

    ## Loads existing session data or creates new
    session_data = load_data_from_json("SESSION_PATH")

    ## Accepts language data from server
    try:
        language, entry = parse_request(['language', 'timestamp', 'active'],
                                        ['CurrentSection', 'CurrentUnit'])
    except ValueError as e:
        logger.error(f"Error updating session info: {str(e)}")
        return f"Error: {str(e)}", 400

    ## Update new entry
    session_data[language] = entry

    ## Marking other languages as inactive
    set_active_session(session_data, language)

    # Write everything back to the JSON file
    write_data_to_json("SESSION_PATH", session_data)

    logger.info(f"'{get_path("SESSION_PATH")}': Session info updated successfully")

    return "Session sent successfully", 200



if __name__ == '__main__':
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("127.0.0.1", PORT))
        except OSError:
            logger.error(f"Port {PORT} is already in use. Exiting.")
            sys.exit(1)

    app.run(port=PORT)