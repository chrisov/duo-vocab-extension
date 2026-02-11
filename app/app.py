import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

SAVE_DIR = "captured_pages"

# @app.route('/log-lesson', methods=['POST'])
# def log_lesson():
#     data = request.get_json(silent=True)
#     if not data or 'unit' not in data or 'level' not in data:
#         return jsonify({"error": "Missing required fields"}), 400

#     unit = data.get('unit')
#     level = data.get('level')
#     timestamp = data.get('timestamp')
#     language = data.get('language', 'Unknown')
    
#     # Load existing session config or create new
#     config_path = "../config/last_session.json"
#     if os.path.exists(config_path):
#         with open(config_path, "r", encoding='utf-8') as f:
#             session_data = json.load(f)
#     else:
#         session_data = {}
    
#     # Update only the current language's entry
#     session_data[language] = {
#         "unit": unit,
#         "level": level,
#         "timestamp": timestamp
#     }
    
#     # Write back to config
#     with open(config_path, "w", encoding='utf-8') as f:
#         json.dump(session_data, f, indent=2, ensure_ascii=False)
    
#     print(f"Updated session: {language} - Unit {unit}, Level {level}")
#     print(f"Config file written to: {config_path}")
#     return jsonify({"status": "logged"}), 200


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



# @app.route('/save-lesson', methods=['POST'])
# def save_lesson_data():
#     data = request.get_json(silent=True)
#     if not data:
#         return jsonify({"error": "Missing or invalid JSON body"}), 400
#     if 'html' not in data or 'url' not in data:
#         return jsonify({"error": "Missing required fields: html, url"}), 400
    
#     # Create a stable folder name for lesson pages
#     page_slug = "lesson"
#     session_dir = os.path.join(SAVE_DIR, page_slug)
    
#     if not os.path.exists(session_dir):
#         os.makedirs(session_dir)

#     # Save the HTML file (pretty-printed for readability)
#     html_path = os.path.join(session_dir, "page_source.html")
#     soup = BeautifulSoup(data['html'], "html.parser")
#     pretty_html = soup.prettify()
    
#     # Wrap long lines manually to keep reasonable width
#     lines = pretty_html.split('\n')
#     formatted_lines = []
#     for line in lines:
#         if len(line) > 100:
#             # For very long lines, try to break at attributes
#             if '<' in line and '=' in line:
#                 # Keep the opening tag short and move attributes down
#                 formatted_lines.append(line[:100].rstrip() + '\n  ' + line[100:].lstrip())
#             else:
#                 formatted_lines.append(line)
#         else:
#             formatted_lines.append(line)
#     pretty_html = '\n'.join(formatted_lines)

#     with open(html_path, "w", encoding='utf-8') as f:
#         f.write(pretty_html)

#     print(f"--- Saved Lesson Page: {data['url']} ---")
#     print(f"Files updated in: {session_dir}")
    
#     return jsonify({"status": "success"}), 200



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
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    app.run(port=5000)