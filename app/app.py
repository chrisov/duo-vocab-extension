from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import safe_load_data, safe_write_data, parse_request

app = Flask(__name__)
CORS(app)

@app.route('/save-vocab', methods=['POST'])
def save_vocab():
    data = request.get_json(silent=True)
    if not data or 'vocabulary' not in data:
        return jsonify({"error": "Missing required field: vocabulary"}), 400
    
    vocabulary = data.get('vocabulary')
    language = data.get('language')
    timestamp = data.get('timestamp')
    
    print(f"[VOCAB] Received {len(vocabulary)} word(s) in {language}")
    print(f"[VOCAB] Words: {vocabulary}")
    print(f"[VOCAB] Timestamp: {timestamp}")
    
    return "Vocab sent succesfully", 200


@app.route('/save-session', methods=['POST'])
def save_session() -> tuple:
    """
    Saves the last session's details on a JSON file.

    :return: The response and its status code.
    :rtype: tuple
    """

    # Load existing session data or create new
    session_data = safe_load_data("SESSION_PATH")

    ## Get data from server
    try:
        language, entry = parse_request(['language', 'timestamp'],
                                        ['CurrentSection', 'CurrentUnit'])
    except ValueError as e:
        return f"error: {str(e)}", 400
    
    ## Update new entry
    session_data[language] = entry
    
    # Write everything back to the JSON file
    safe_write_data("SESSION_PATH", session_data)
    
    return "Session sent successfully", 200

if __name__ == '__main__':
    app.run(port=5000)