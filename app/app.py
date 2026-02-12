from flask import Flask
from flask_cors import CORS
from utils import safe_load_json, safe_write_json, parse_request

app = Flask(__name__)
CORS(app)

@app.route('/save-vocab', methods=['POST'])
def save_vocab() -> tuple:
    """
    Saves extracted vocab to a JSON file.

    :return: The response and its status code.
    :rtype: tuple
    """

    vocab_data = safe_load_json("VOCAB_PATH")

    try:
        language, entry = parse_request(['language', 'timestamp', 'vocabulary'])
    except ValueError as e:
        return f"Error: {str(e)}", 400

    vocab_data[language] = entry

    safe_write_json("VOCAB_PATH", vocab_data)
    
    return "Vocab sent succesfully", 200


@app.route('/save-session', methods=['POST'])
def save_session() -> tuple:
    """
    Saves the last session's details on a JSON file.

    :return: The response and its status code.
    :rtype: tuple
    """

    # Loads existing session data or creates new
    session_data = safe_load_json("SESSION_PATH")

    ## Get data from server
    try:
        language, entry = parse_request(['language', 'timestamp'],
                                        ['CurrentSection', 'CurrentUnit'])
    except ValueError as e:
        return f"Error: {str(e)}", 400

    ## Update new entry
    session_data[language] = entry

    # Write everything back to the JSON file
    safe_write_json("SESSION_PATH", session_data)

    return "Session sent successfully", 200

if __name__ == '__main__':
    app.run(port=5000)