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

# Build KMP partial match table for pattern
def build_kmp_table(pattern):
    if not pattern:
        return []
    
    table = [0] * len(pattern)
    j = 0
    
    # Loop to build table
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = table[j - 1]  # Fallback in table
        
        if pattern[i] == pattern[j]:
            j += 1
            table[i] = j
        else:
            table[i] = 0
    
    return table

# KMP search to find all positions of pattern in text
def kmp_search_with_positions(text, pattern):
    positions = []  # Stores all start positions of matches
    
    if not pattern:
        return positions
    
    text_lower = text.lower()
    pattern_lower = pattern.lower()
    
    n = len(text_lower)
    m = len(pattern_lower)
    
    if m > n:
        return positions
    
    kmp_table = build_kmp_table(pattern_lower)
    
    j = 0
    for i in range(n):
        while j > 0 and text_lower[i] != pattern_lower[j]:
            j = kmp_table[j - 1]
        
        if text_lower[i] == pattern_lower[j]:
            j += 1
        
        if j == m:
            start_pos = i - m + 1
            positions.append(start_pos)
            j = kmp_table[j - 1]
    
    return positions

# Highlight all occurrences of pattern in text
def highlight_word(text, pattern):
    if not pattern:
        return text
    
    red_color = "\033[91m"
    reset_color = "\033[0m"
    positions = kmp_search_with_positions(text, pattern)
    
    if not positions:
        return text
    
    result = []
    last_pos = 0
    
    # Add colored segments to result
    for pos in positions:
        result.append(text[last_pos:pos])
        result.append(f"{red_color}{text[pos:pos+len(pattern)]}{reset_color}")
        last_pos = pos + len(pattern)
    
    result.append(text[last_pos:])
    return "".join(result)

# Search all Bible verses for a word
def search_and_highlight(search_word):
    results = []
    
    for book in k.bible['books']:
        for chapter in book['chapters']:
            for verse in chapter['verses']:
                verse_text = verse['text']
                
                # Use KMP to check if word exists
                if kmp_search_with_positions(verse_text, search_word):
                    results.append({
                        'book': book['name'],
                        'chapter': chapter['chapter'],
                        'verse': verse['verse'],
                        'text': verse_text
                    })
    
    return results

# Display results with the search word highlighted
def display_highlighted_results(results, search_word):
    if not results:
        print(f"\nNo results found for '{search_word}'")
        return
    
    print(f"\nFound {len(results)} results for '{search_word}':")
    print("=" * 60)
    
    for result in results:
        book = result['book']
        chapter = result['chapter']
        verse = result['verse']
        text = result['text']
        
        highlighted_text = highlight_word(text, search_word)  # Highlight word
        
        print(f"{book} {chapter}:{verse}")
        print(f"  {highlighted_text}")
        print("-" * 60)

# Main program loop
def main():
    print("=== BIBLE WORD SEARCH WITH HIGHLIGHTING ===")
    
    while True:
        print("\nOptions: [1] Search word  [2] View history  [3] Exit")
        choice = input("Choose option (1-3): ").strip()
        
        if choice == "1":
            search_word = input("Enter word to search: ").strip()
            if not search_word:
                print("Please enter a word.")
                continue
            
            print(f"\nSearching for '{search_word}'...")
            results = search_and_highlight(search_word)  # Perform search
            display_highlighted_results(results, search_word)  # Show results
            
            add_to_history(search_word, len(results))  # Save to history
            
        elif choice == "2":
            show_search_history()  # Display search history
            
        elif choice == "3":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Run the program
if __name__ == "__main__":
    main()
