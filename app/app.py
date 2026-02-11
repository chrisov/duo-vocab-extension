import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

SAVE_DIR = "captured_pages"

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
    
    return jsonify({
        "status": "success",
        "words_received": len(vocabulary),
        "language": language
    }), 200

@app.route('/save-session', methods=['POST'])
def save_session():
    data = request.get_json(silent=True)
    if not data or 'language' not in data:
        return jsonify({"error": "Missing required field: language"}), 400

    language = data.get('language')
    current_section = data.get('currentSection')  # Optional for now
    current_unit = data.get('currentUnit')  # Optional for now
    timestamp = data.get('timestamp')
    
    # Load existing session data or create new
    config_path = "../config/session.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding='utf-8') as f:
                session_data = json.load(f)
        except json.JSONDecodeError:
            session_data = {}
    else:
        session_data = {}
    
    # Build entry - only include section/unit if provided
    entry = {"timestamp": timestamp}
    if current_section is not None:
        entry["currentSection"] = current_section
    if current_unit is not None:
        entry["currentUnit"] = current_unit
    
    # Update only the current language's entry (preserving other languages)
    session_data[language] = entry
    
    # Write back to config
    os.makedirs("../config", exist_ok=True)
    with open(config_path, "w", encoding='utf-8') as f:
        json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    print(f"Updated session info: {language} - Section {current_section}, Unit {current_unit}")
    print(f"Session file written to: {config_path}")
    return jsonify({
        "status": "success", 
        "language": language, 
        "currentSection": current_section,
        "currentUnit": current_unit
    }), 200



@app.route('/save-vocabulary', methods=['POST'])
def save_vocabulary():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Missing or invalid JSON body"}), 400
    if 'words' not in data:
        return jsonify({"error": "Missing required field: words"}), 400

    # Use config directory for vocabulary file
    vocab_file = "../config/spanish_words.json"
    if os.path.exists(vocab_file):
        try:
            if os.path.getsize(vocab_file) == 0:
                vocabulary = {}
            else:
                with open(vocab_file, "r", encoding='utf-8') as f:
                    vocabulary = json.load(f)
        except json.JSONDecodeError:
            vocabulary = {}
    else:
        vocabulary = {}

    # Ensure Spanish key exists
    existing_entries = vocabulary.get("es", [])
    existing_pairs = {(e.get("word"), e.get("class")) for e in existing_entries if isinstance(e, dict)}

    # Add new words (deduplicated by word + class)
    new_entries = []
    for word_data in data['words']:
        word = (word_data.get('word') or '').strip()
        class_name = (word_data.get('class') or '').strip()
        if not word:
            continue

        pair = (word, class_name)
        if pair in existing_pairs:
            continue

        entry = {
            "word": word,
            "class": class_name,
            "dataTest": (word_data.get('dataTest') or '').strip()
        }
        existing_entries.append(entry)
        existing_pairs.add(pair)
        new_entries.append(entry)

    vocabulary["es"] = existing_entries

    # Save to file
    with open(vocab_file, "w", encoding='utf-8') as f:
        json.dump(vocabulary, f, indent=2, ensure_ascii=False)

    print(f"--- Added {len(new_entries)} new Spanish word(s) ---")
    if new_entries:
        print(f"New words: {[e['word'] for e in new_entries]}")
    print(f"Total unique Spanish word entries: {len(vocabulary['es'])}")

    return jsonify({
        "status": "success",
        "words_added": len(new_entries),
        "total_unique": len(vocabulary["es"])
    }), 200

if __name__ == '__main__':
    app.run(port=5000)