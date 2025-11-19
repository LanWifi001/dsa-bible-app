import KJV as k
import json
import os
from datetime import datetime
from utils import ascii_box, clear

# History file name
HISTORY_FILE = "bible_history.json"

def load_search_history():
    """Load search history from JSON file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                # Make sure it's a list
                if isinstance(history, list):
                    return history
        # Return empty list if file doesn't exist or is invalid
        return []
    except Exception as e:
        print(f"Warning: Could not load history - {e}")
        return []

def save_search_history(history):
    """Save search history to JSON file"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        # Print confirmation (can be removed later)
        print(f"Search saved to history: {HISTORY_FILE}")
    except Exception as e:
        print(f"Error: Could not save history - {e}")

def clear_history():
    clear()
    cleared = load_search_history()


    print(ascii_box(['Do you want to clear the search history? y/n'], title = 'Clear Search History', padding=2, align='left'))
    user = input('> ')

    while user.lower() not in 'yn':
        clear()
        print(ascii_box(['Do you want to clear the search history? y/n'], title = 'Clear Search History', padding=2, align='left'))
        user = input('Invalid Input. y or n only:')
    
    if user.lower() == 'n':
        return
    elif user.lower() == 'y':
        cleared.clear()
        save_search_history(cleared)
        clear()
        print(ascii_box(['Search History Cleared. Press enter to go back.'], title = 'Clear Search History', padding=2, align='left'))
        user = input()

        while user != '':
            clear()
            print(ascii_box(['Invalid input. Press enter to go back.'], title = 'Clear Search History', padding=2, align='left'))
            user = input()
        if user == '':
            return

def add_to_history(search_word, results_count):
    """Add search to history"""
    history = load_search_history()
    
    search_entry = {
        "word": search_word,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results_count
    }
    
    # Add to beginning so newest appears first
    history.insert(0, search_entry)
    
    # Keep only last 100 searches
    if len(history) > 100:
        history = history[:100]
    
    save_search_history(history)

def show_search_history():
    """Display search history"""
    history = load_search_history()
    
    if not history:
        print("\nNo search history found.")
        return
    
    print(ascii_box([f"Search History ({len(history)} entries)"], title = 'Word Search', padding=2, align='left'))
    for i, entry in enumerate(history, 1):
        print(f"{i}. '{entry['word']}' - {entry['results']} results ({entry['timestamp']})")

def build_kmp_table(pattern):
    """
    Build the partial match table for KMP algorithm
    """
    if not pattern:
        return []
    
    table = [0] * len(pattern)
    j = 0
    
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = table[j - 1]
        
        if pattern[i] == pattern[j]:
            j += 1
            table[i] = j
        else:
            table[i] = 0
    
    return table

def kmp_search_with_positions(text, pattern):
    """
    Search for pattern in text using KMP algorithm
    Returns list of start positions where pattern is found
    """
    positions = []
    
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

def highlight_word(text, pattern):
    """
    Highlight the pattern in text with red color
    """
    if not pattern:
        return text
    
    red_color = "\033[91m"
    reset_color = "\033[0m"
    positions = kmp_search_with_positions(text, pattern)
    
    if not positions:
        return text
    
    result = []
    last_pos = 0
    
    for pos in positions:
        result.append(text[last_pos:pos])
        result.append(f"{red_color}{text[pos:pos+len(pattern)]}{reset_color}")
        last_pos = pos + len(pattern)
    
    result.append(text[last_pos:])
    return "".join(result)

def search_and_highlight(search_word):
    """
    Search for word in all Bible verses and highlight matches
    """
    results = []
    
    for book in k.bible['books']:
        for chapter in book['chapters']:
            for verse in chapter['verses']:
                verse_text = verse['text']
                
                # Check if word exists in verse using KMP
                if kmp_search_with_positions(verse_text, search_word):
                    results.append({
                        'book': book['name'],
                        'chapter': chapter['chapter'],
                        'verse': verse['verse'],
                        'text': verse_text
                    })
    
    return results

def display_highlighted_results(results, search_word):
    """
    Display results with highlighted search word
    """
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
        
        # Highlight the search word in the verse text
        highlighted_text = highlight_word(text, search_word)
        
        print(f"{book} {chapter}:{verse}")
        print(f"  {highlighted_text}")
        print("-" * 60)

# Main program
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
            results = search_and_highlight(search_word)
            display_highlighted_results(results, search_word)
            
            # Add to history
            add_to_history(search_word, len(results))
            
        elif choice == "2":
            show_search_history()
            
        elif choice == "3":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Run the program
if __name__ == "__main__":
    main()