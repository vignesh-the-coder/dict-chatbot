import tkinter as tk
from tkinter import messagebox, ttk
import json

def load_dictionary():
    try:
        with open("dictionary.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def search_word():
    word = entry_word.get().lower()
    dictionary = load_dictionary()
    meaning = dictionary.get(word, "Word not found")
    text_result.delete(1.0, tk.END)  # Clear previous result
    text_result.insert(tk.END, meaning)  # Insert new result
    animate_label()

def add_word():
    word = entry_word.get().lower()
    meaning = entry_meaning.get()
    if word and meaning:
        dictionary = load_dictionary()
        dictionary[word] = meaning
        with open("dictionary.json", "w") as file:
            json.dump(dictionary, file, indent=4)
        messagebox.showinfo("Success", f"Word '{word}' added successfully!")
        entry_meaning.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter both word and meaning.")

def animate_label():
    current_text = text_result.get(1.0, tk.END)
    text_result.delete(1.0, tk.END)
    text_result.after(100, lambda: text_result.insert(tk.END, current_text))

# GUI setup
root = tk.Tk()
root.title("Dictionary Chatbot")

# Window size
root.geometry("800x600")
root.resizable(True, True)

# Styling
root.configure(bg="#f4f4f9")
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TEntry", font=("Arial", 14), padding=10)

# Input fields
frame_input = tk.Frame(root, bg="#f4f4f9")
frame_input.pack(pady=20)

tk.Label(frame_input, text="Enter Word:", bg="#f4f4f9", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10)
entry_word = ttk.Entry(frame_input, font=("Arial", 14))
entry_word.grid(row=0, column=1, padx=10, pady=10, ipadx=20)

tk.Label(frame_input, text="Enter Meaning (if adding):", bg="#f4f4f9", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=10)
entry_meaning = ttk.Entry(frame_input, font=("Arial", 14))
entry_meaning.grid(row=1, column=1, padx=10, pady=10, ipadx=20)

# Buttons
frame_buttons = tk.Frame(root, bg="#f4f4f9")
frame_buttons.pack(pady=20)

btn_search = ttk.Button(frame_buttons, text="Search Meaning", command=search_word)
btn_search.grid(row=0, column=0, padx=20, pady=10)

btn_add = ttk.Button(frame_buttons, text="Add Word", command=add_word)
btn_add.grid(row=0, column=1, padx=20, pady=10)

# Output label with larger font (using Text widget for full meaning)
text_result = tk.Text(root, height=10, width=70, wrap=tk.WORD, font=("Arial", 16), bg="#f4f4f9", bd=2, relief="sunken")
text_result.pack(pady=30)

# Run GUI
root.mainloop()
