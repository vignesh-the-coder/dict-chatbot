import json
import nltk
from nltk.corpus import wordnet
from nltk.chat.util import Chat, reflections

# Download WordNet if not already available
nltk.download('wordnet')

# File to store dictionary
DICTIONARY_FILE = "dictionary.json"

# Load dictionary from file
def load_dictionary():
    try:
        with open(DICTIONARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return empty dictionary if file doesn't exist

# Save dictionary to file
def save_dictionary(dictionary):
    with open(DICTIONARY_FILE, "w") as file:
        json.dump(dictionary, file, indent=4)

# Fetch meaning of a word
def get_meaning(word):
    dictionary = load_dictionary()
    word = word.lower()

    if word in dictionary:
        return dictionary[word]  # Return stored meaning
    
    # If not found in user dictionary, fetch from WordNet
    synsets = wordnet.synsets(word)
    if synsets:
        return synsets[0].definition()  # Fetch definition safely
    
    return "Sorry, I couldn't find the meaning of that word."

# Add or update word in dictionary
def update_dictionary(word, meaning):
    dictionary = load_dictionary()
    dictionary[word.lower()] = meaning
    save_dictionary(dictionary)
    return f"Word '{word}' added/updated successfully!"

# Define chatbot responses (only static responses here)
pairs = [
    [r"hello|hi|hey", ["Hello! How can I assist you today?"]],
    [r"bye", ["Goodbye! Have a great day!"]],
]

# Initialize chatbot
chatbot = Chat(pairs, reflections)

# Function to handle user input manually
def process_user_input(user_input):
    user_input = user_input.lower().strip()

    # Handle dictionary queries separately
    if user_input.startswith("what is meaning of ") or user_input.startswith("what is the meaning of "):
        word = user_input.split("of")[-1].strip()
        return get_meaning(word)
    
    # Handle word addition separately
    if user_input.startswith("add word "):
        try:
            _, word_part, meaning_part = user_input.split("word ", 1)[1].split(" meaning ", 1)
            return update_dictionary(word_part.strip(), meaning_part.strip())
        except ValueError:
            return "Invalid format! Use: add word <word> meaning <meaning>"
    
    # For static responses, use the chatbot
    return chatbot.respond(user_input) or "I'm sorry, I didn't understand that."

# Run chatbot
def start_chat():
    print("\nDictionary Chatbot: Type 'bye' to exit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "bye":
            print("Dictionary Chatbot: Goodbye! Have a great day! 👋")
            break
        
        response = process_user_input(user_input)
        print(f"Dictionary Chatbot: {response}")

if __name__ == "__main__":
    start_chat()
