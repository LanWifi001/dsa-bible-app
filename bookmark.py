import KJV as b          # Import the KJV Bible data; aliased as 'b' for convenience
import json              # To save/load bookmarks in JSON format
from utils import ascii_box, clear  # Utility functions: ascii_box for formatting, clear to clear terminal
import color as c        # Color constants for terminal text styling

# ---------------------------------------
# Function: run_bookmark
# Description: Handles the process of adding a bookmark.
#  - Loads existing bookmarks from bookmark.json
#  - Validates user input
#  - Prevents duplicate bookmarks
#  - Writes updated bookmarks back to the JSON file
# ---------------------------------------
def run_bookmark():
    # opens the bookmark.json file as bookmark
    try:
        with open('bookmark.json', 'r') as file:
            bookmark = json.load(file)
    except FileNotFoundError:
        bookmark = {} 

    # Loop to keep adding bookmarks until user exits
    while True:
        # holds the user bookmark array from input
        user = user_bookmark()
        user_str = str(user)

        # if the user decides to exit the bookmark loop, the function stops
        if user_str.lower() == 'exit':
           break

        # if the verse doesn't exist
        if user == 'not found':
            continue
        
        # ensures that each bookmark doesn't repeat using a unique key
        key = f"{user['book']}-{user['chapter']}-{user['verse']}" 
        if key in bookmark:  # check for duplicate
            clear()
            print('Bookmark already exists.')
            continue
        
        # if it is not yet in the bookmarks and exists
        else:
            clear()
            print('Bookmark added!')
            bookmark[key] = user 
    
    # Write the updated bookmarks back to bookmark.json
    with open('bookmark.json', 'w') as file:
        json.dump(bookmark, file, indent = 4) 
        

# ---------------------------------------
# Function: user_bookmark
# Description: Handles user input for adding a bookmark.
#  - Displays instructions
#  - Validates input format
#  - Checks if the verse exists in the Bible data
#  - Returns a bookmark dictionary, 'exit', or 'not found'
# ---------------------------------------
def user_bookmark():
    # instructions for bookmarking a verse
    print(c.CYAN)
    print(ascii_box(['Add a verse to bookmark or', 'Press enter to exit'], title='Add a Bookmark', padding=2, align='left'))
    print(c.RESET)
    print('Enter with this format (Genesis 1 1)')
    user = input('> ').strip()

    # Check if user wants to exit
    if user == '':
        return 'exit'
    else:
        user_arr = user.split()

        # Validate input length (must have 3 parts: book, chapter, verse)
        if len(user_arr) != 3:
            clear()
            print('Invalid Input!')
            return 'not found'

        # Extract book, chapter, and verse from input
        book = user_arr[0]
        chapter = int(user_arr[1])
        verse = int(user_arr[2])
        
        # Check if the user's input exists in the Bible
        for i in b.bible['books']:
            if i['name'].lower() == book.lower():
                for j in i['chapters']:
                    if j['chapter'] == chapter:
                        for k in j['verses']:
                            if k['verse'] == verse:
                                # Create the bookmark dictionary and return
                                bookmark = create_bookmark(user_arr)
                                return bookmark
        else:
            clear()
            print('Verse not found.')
            return 'not found'

# ---------------------------------------
# Function: create_bookmark
# Description: Generates a bookmark dictionary from a list of inputs
#  - Input: [book, chapter, verse]
#  - Returns: {'book': ..., 'chapter': ..., 'verse': ...}
# ---------------------------------------
def create_bookmark(arr):
    # Initialize placeholders
    book = ''
    chapter = 0
    verse = 0

    # Map input array to respective fields
    for i in range(len(arr)):
        if i == 0:
            book = arr[i].title()
        elif i == 1:
            chapter = int(arr[i])
        elif i == 2:
            verse = int(arr[i])
        else:
            break
    
    # Return dictionary to be stored as a bookmark
    return {
        'book': book,
        'chapter': chapter,
        'verse': verse
    }

# ---------------------------------------
# Function: get_verse
# Description: Displays saved bookmarks and lets the user view the text
#  - Loads bookmarks
#  - Shows numbered list
#  - Lets user select a verse
#  - Displays the verse text in ascii_box
# ---------------------------------------
def get_verse():
    # Load bookmarks from JSON
    try:
        with open('bookmark.json', 'r') as file:
            bookmark = json.load(file)
    except FileNotFoundError:
        bookmark = {}

    # Handle empty bookmarks
    if len(bookmark) == 0:
        print(c.YELLOW)
        print(ascii_box(['You have no bookmarks yet', 'Press enter to go back.'], title='No Bookmarks', padding=2, align='left'))
        print(c.RESET)        
        user_input = input().strip()
        while user_input != '':
            clear()
            print(c.CYAN)
            print(ascii_box(['You have no bookmarks yet', 'Press enter to go back.'], title='No Bookmarks', padding=2, align='left'))
            print(c.RESET)            
            user_input = input('Invalid input, number only, press enter.').strip()
        if user_input == '':
            return

    # Prepare a numbered list of bookmarks
    verses = []
    keys = list(bookmark.keys())  # Get keys for indexing
    for idx, key in enumerate(keys):
        value = bookmark[key]
        verses.append(f"{idx+1}. {value['book']} {value['chapter']}:{value['verse']}")
    print(c.CYAN)    
    print(ascii_box(verses, title='Bookmarks', padding=2, align='left'))
    print(c.RESET)

    # Get user selection
    user_input = input('Input the verse number to view or press "q" to return: ').strip()
    while user_input.isdigit() == False and user_input.lower() != 'q':
        clear()
        print(c.CYAN)    
        print(ascii_box(verses, title='Bookmarks', padding=2, align='left'))
        print(c.RESET)
        user_input = input('Invalid input, number only or press "q" to return: ').strip()
    if user_input.lower() == 'q':
        return

    # Convert input to index
    user_idx = int(user_input) - 1
    if user_idx < 0 or user_idx >= len(keys):
        print("Invalid verse number.")
        return

    # Retrieve bookmark by hash key
    user_verse_data = bookmark[keys[user_idx]]
    in1 = user_verse_data['book']
    in2 = int(user_verse_data['chapter'])
    in3 = int(user_verse_data['verse'])

    # Find the verse text in Bible data
    verse = []
    for i in b.bible['books']:
        if i['name'] == in1:
            chapter_data = i['chapters'][in2 - 1]
            verse_data = chapter_data['verses'][in3 - 1]
            clear()
            verse.append(f'{in1} {in2}:{in3}')
            verse.append(verse_data['text'])
    print(c.CYAN)    
    print(ascii_box([verse[1]], title=verse[0], padding=2, align='left'))
    print(c.RESET)

    # Wait for user to go back
    user = input('Press enter to go back.').strip()
    while user != '':
        user = input('Invalid Input, press enter.').strip()
    if user == '':
        return

# ---------------------------------------
# Function: remove_bookmark
# Description: Lets the user delete a saved bookmark
#  - Displays bookmarks
#  - Prompts user to select one to remove
#  - Updates the JSON file
# ---------------------------------------
def remove_bookmark():
    # Load bookmarks from JSON
    try:
        with open('bookmark.json', 'r') as file:
            bookmark = json.load(file)
    except FileNotFoundError:
        bookmark = {}

    # Handle empty bookmarks
    if len(bookmark) == 0:
        print(c.YELLOW)
        print(ascii_box(['You have no bookmarks yet', 'Press enter to go back.'], title='No Bookmarks', padding=2, align='left'))
        print(c.RESET)       
        user_input = input().strip()
        while user_input != '':
            clear()
            print(c.YELLOW)    
            print(ascii_box(['You have no bookmarks yet', 'Press enter to go back.'], title='No Bookmarks', padding=2, align='left'))
            print(c.RESET)    
            user_input = input('Invalid input, number only, press enter.').strip()
        if user_input == '':
            return

    # Display all bookmarks
    verses = []
    keys = list(bookmark.keys())
    for idx, key in enumerate(keys):
        value = bookmark[key]
        verses.append(f"{idx+1}. {value['book']} {value['chapter']}:{value['verse']}")
    print(c.CYAN)    
    print(ascii_box(verses, title='Bookmarks', padding=2, align='left'))
    print(c.RESET)

    # Get user input for deletion
    user_input = input('Input bookmark number to remove, or press enter to exit: ').strip()
    while user_input != '' and user_input.isdigit() == False:
        clear()
        print(c.CYAN)    
        print(ascii_box(verses, title='Bookmarks', padding=2, align='left'))
        print(c.RESET)
        user_input = input('Invalid input, number only, or press enter to exit: ').strip()
    if user_input == '':
        return

    # Convert input to index
    user_idx = int(user_input) - 1
    if user_idx < 0 or user_idx >= len(keys):
        print("Invalid bookmark number.")
        return

    clear()
    print(c.CYAN)    
    print(ascii_box(verses, title='Bookmarks', padding=2, align='left'))
    print(c.RESET)

    # Delete the selected bookmark by key
    del bookmark[keys[user_idx]]

    # Save updated bookmarks
    with open('bookmark.json', 'w') as file:
        json.dump(bookmark, file, indent = 4)
    
    print('Bookmark removed! Press enter to return.')
    user = input().strip()
    while user != '':
        clear()
        print(c.CYAN)    
        print(ascii_box(verses, title='Bookmarks', padding=2, align='left'))
        print(c.RESET)
        print('Invalid Input! Press enter to return.')
        user = input().strip()
    if user == '':
        return

# ---------------------------------------
# Function: clear_bookmarks
# Description: Clears all bookmarks after user confirmation
# ---------------------------------------
def clear_bookmarks():
    # Load bookmarks from JSON
    try:
        with open('bookmark.json', 'r') as file:
            bookmarks = json.load(file)
    except FileNotFoundError:
        bookmarks = {}

    # Ask user for confirmation
    print(c.RED)
    print(ascii_box(['Are you sure, you want to clear the bookmarks? y/n: '], title="Clear Bookmark", padding=2, align='left'))
    print(c.RESET)    
    user = input('> ').strip()
    while user.lower() not in 'yn':
        user = input('Invalid Input, y or n only: ').strip()
    
    if user.lower() == 'n':
        return
    elif user.lower() == 'y':
        bookmarks.clear()

        # Save empty bookmarks
        with open('bookmark.json', 'w') as file:
            json.dump(bookmarks, file)
        clear()
        print(c.GREEN)
        print(ascii_box(['Bookmarks cleared, press enter to go back.'], title="Clear Bookmark", padding=2, align='left'))
        print(c.RESET)        
        input().strip()

# ---------------------------------------
# Function: add_bookmark
# Description: Adds a bookmark directly from book, chapter, verse arguments
#  - Prevents duplicates using unique hash key
#  - Saves to JSON file
# ---------------------------------------
def add_bookmark(idx1, idx2, idx3):
    book = idx1
    chapter = int(idx2)
    verse = int(idx3)

    key = f"{book}-{chapter}-{verse}"  # Unique key for hash table
    bookmark_entry = create_bookmark([book, chapter, verse])

    # Load bookmarks
    try:
        with open('bookmark.json', 'r') as file:
            bookmark = json.load(file)
    except FileNotFoundError:
        bookmark = {}

    # Check for duplicate
    if key in bookmark:
        print('Bookmark already exists.')
    else:
        bookmark[key] = bookmark_entry  # Add new bookmark

        # Save updated bookmarks
        with open('bookmark.json', 'w') as file:
            json.dump(bookmark, file, indent=4)
        print('Bookmark Added.')
    return input('Press enter to continue.').strip()

# ---------------------------------------
# Function: start_bm
# Description: Displays bookmark menu and handles user choices
#  - View bookmarks
#  - Add bookmarks
#  - Remove bookmarks
#  - Clear bookmarks
#  - Exit to main menu
# ---------------------------------------
def start_bm():
    while True:
        bm_menu = ['Input the number you want to do',
        '1. View Bookmarks',
        '2. Add Bookmarks',
        '3. Remove Bookmarks',
        '4. Clear Bookmars',
        '5. Back']
        print(c.CYAN)    
        print(ascii_box(bm_menu, title="Bookmarks Menu", padding=2, align='left'))
        print(c.RESET)

        # Get user input
        user = input('Your Input: ').strip()
        while user.isdigit() == False:
            clear()
            print(c.CYAN)
            print(ascii_box(bm_menu, title="Bookmarks Menu", padding=2, align='left'))
            print(c.RESET)    
            user = input('Invalid Input. Numbers only: ').strip()
        
        user_int = int(user)
        clear()

        # Handle user choice
        match user_int:
            case 1:
                get_verse()
                clear()
            case 2:
                run_bookmark()
                clear()
            case 3:
                remove_bookmark()
                clear()
            case 4:
                clear_bookmarks()
                clear()
            case 5:
                return
            case _:
                print('Invalid Input.')
