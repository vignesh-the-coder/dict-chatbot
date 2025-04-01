from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load dictionary
def load_dictionary():
    with open("dictionary.json", "r") as file:
        return json.load(file)

# Search word meaning
@app.route('/search', methods=['GET'])
def search_word():
    word = request.args.get('word', '').lower()
    dictionary = load_dictionary()
    meaning = dictionary.get(word, "Word not found")
    return jsonify({"word": word, "meaning": meaning})

# Add/update word
@app.route('/update', methods=['POST'])
def update_word():
    data = request.json
    word = data.get("word", "").lower()
    meaning = data.get("meaning", "")
    
    dictionary = load_dictionary()
    dictionary[word] = meaning
    
    with open("dictionary.json", "w") as file:
        json.dump(dictionary, file, indent=4)
    
    return jsonify({"message": f"Word '{word}' updated successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
