import KJV as k           # Bible data to reference during searches
import json               # Save/load history in JSON
import os                 # File handling, e.g., check if history file exists
from datetime import datetime  # Timestamp each search
from utils import ascii_box, clear  # Nicely format search history and clear screen
import color as c         # Terminal text colors

# File to store search history
HISTORY_FILE = "bible_history.json"

# Load search history from JSON file
def load_search_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                # Ensure loaded data is a list
                if isinstance(history, list):
                    return history
        # Return empty list if file doesn't exist or invalid
        return []
    except Exception as e:
        print(f"Warning: Could not load history - {e}")
        return []

# Save search history to JSON file
def save_search_history(history):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        # Confirmation message (optional)
        print(f"Search saved to history: {HISTORY_FILE}")
    except Exception as e:
        print(f"Error: Could not save history - {e}")

# Clear the search history
def clear_history():
    clear()
    cleared = load_search_history()

    # Ask user for confirmation
    print(c.RED)
    print(ascii_box(['Do you want to clear the search history? y/n'], title='Clear Search History', padding=2, align='left'))
    print(c.RESET)
    user = input('> ').strip()

    # Validate input (only y/n)
    while user.lower() not in 'yn':
        clear()
        print(c.RED)
        print(ascii_box(['Do you want to clear the search history? y/n'], title='Clear Search History', padding=2, align='left'))
        print(c.RESET)
        user = input('Invalid Input. y or n only:').strip()
    
    if user.lower() == 'n':
        return
    elif user.lower() == 'y':
        cleared.clear()  # Clear history list
        save_search_history(cleared)  # Save empty list
        clear()
        print(c.GREEN)
        print(ascii_box(['Search History Cleared. Press enter to go back.'], title='Clear Search History', padding=2, align='left'))
        print(c.RESET)
        user = input().strip()

        # Ensure user presses enter
        while user != '':
            clear()
            print(c.CYAN)
            print(ascii_box(['Invalid input. Press enter to go back.'], title='Clear Search History', padding=2, align='left'))
            print(c.RESET)
            user = input().strip()
        if user == '':
            return

# Add a search entry to history
def add_to_history(search_word, results_count):
    history = load_search_history()  # Load existing history
    
    # Create new search entry
    search_entry = {
        "word": search_word,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results_count
    }
    
    # Add new search at the beginning (latest first)
    history.insert(0, search_entry)
    
    # Keep only last 100 searches
    if len(history) > 100:
        history = history[:100]
    
    save_search_history(history)  # Save updated history

# Show all search history
def show_search_history():
    history = load_search_history()  # Load existing history
    
    # If no history found
    if not history:
        print(c.CYAN)
        print(ascii_box([f"Search History ({len(history)} entries)"], title='No search history found', padding=2, align='left'))
        print(c.RESET)
        return
    
    # Display history with number, word, result count, and timestamp
    print(c.CYAN)
    print(ascii_box([f"Search History ({len(history)} entries)"], title='Word Search', padding=2, align='left'))
    print(c.RESET)
    for i, entry in enumerate(history, 1):
        print(f"{i}. '{entry['word']}' - {entry['results']} results ({entry['timestamp']})")
