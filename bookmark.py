import KJV as b
import json
from utils import ascii_box, clear
import color as c

# runs the bookmark function
def run_bookmark():
    # opens the bookmark.json file as bookmark
    try:
        with open('bookmark.json', 'r') as file:
            bookmark = json.load(file)
    except FileNotFoundError:
        bookmark = {}  # changed to dict for hash table

    # user input validation
    while True:
        # holds the user bookmark array
        user = user_bookmark()

        # if the user decides to exit the bookmark loop, the function stops
        if user.lower() == 'exit':
           break

        # if the verse doesn't exist
        if user == 'not found':
            continue
        
        # ensures that each bookmark doesn't repeat
        key = f"{user['book']}-{user['chapter']}-{user['verse']}"  # new: unique hash key
        if key in bookmark:  # changed to dict lookup
            clear()
            print('Bookmark already exists.')
            continue
        
        # if it is not yet in the bookmarks and exists
        else:
            clear()
            print('Bookmark added!')
            bookmark[key] = user  # changed: store in dict with hash key
    
    # opens the json file again and dumps the bookmarks
    with open('bookmark.json', 'w') as file:
        json.dump(bookmark, file, indent = 4)  # hash table dict saved
        

# handles user inputs for bookmarking
def user_bookmark():
    print(c.CYAN)
    print(ascii_box(['Add a verse to bookmark or', 'Press enter to exit.'], title='Add a Bookmark', padding=2, align='left'))
    print(c.RESET)
    user = input('> ')

    if user == '':
        return 'exit'
    else:
        user_arr = user.split()

        if len(user_arr) != 3:
            clear()
            print('Invalid Input!')
            return 'not found'

        book = user_arr[0]
        chapter = int(user_arr[1])
        verse = int(user_arr[2])
        
        for i in b.bible['books']:
            if i['name'] == book:
                for j in i['chapters']:
                    if j['chapter'] == chapter:
                        for k in j['verses']:
                            if k['verse'] == verse:
                                bookmark = create_bookmark(user_arr)
                                return bookmark
        else:
            print('Verse not found.')
            return 'not found'

# function that handles the creation of the bookmark based from the users input
def create_bookmark(dict):
    book = ''
    chapter = 0
    verse = 0
    for i in range(len(dict)):
        if i == 0:
            book = dict[i]
        elif i == 1:
            chapter = int(dict[i])
        elif i == 2:
            verse = int(dict[i])
        else:
            break
    return {
        'book': book,
        'chapter': chapter,
        'verse': verse
    }

# function to get a verse
def get_verse():
    try:
        with open('bookmark.json', 'r') as file:
            bookmark = json.load(file)
    except FileNotFoundError:
        bookmark = {}

    if len(bookmark) == 0:
        print(c.YELLOW)
        print(ascii_box(['You have no bookmarks yet', 'Press enter to go back.'], title='No Bookmarks', padding=2, align='left'))
        print(c.RESET)        
        user_input = input()
        while user_input != '':
            clear()
            print(c.CYAN)
            print(ascii_box(['You have no bookmarks yet', 'Press enter to go back.'], title='No Bookmarks', padding=2, align='left'))
            print(c.RESET)            
            user_input = input('Invalid input, number only, press enter.')
        if user_input == '':
            return

    verses = []
    keys = list(bookmark.keys())  # changed: get keys for indexing
    for idx, key in enumerate(keys):
        value = bookmark[key]
        verses.append(f"{idx+1}. {value['book']} {value['chapter']}:{value['verse']}")
    print(c.CYAN)    
    print(ascii_box(verses, title='Bookmarks', padding=2, align='left'))
    print(c.RESET)
    user_input = input('Input the verse number to view or exit: ')
    if user_input.lower() == 'exit':
        return
    
    while user_input.isdigit() == False:
        user_input = input('Invalid input, number only: ')

    user_idx = int(user_input) - 1
    if user_idx < 0 or user_idx >= len(keys):
        print("Invalid verse number.")
        return

    user_verse_data = bookmark[keys[user_idx]]  # changed: access by hash key

    in1 = user_verse_data['book']
    in2 = int(user_verse_data['chapter'])
    in3 = int(user_verse_data['verse'])

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
    user = input('\nPress enter to go back.')

    while user != '':
        user = input('Invalid Input, press enter.')

    if user == '':
        return

# function that removes a bookmark based on the users preferences
def remove_bookmark():
    try:
        with open('bookmark.json', 'r') as file:
            bookmark = json.load(file)
    except FileNotFoundError:
        bookmark = {}

    if len(bookmark) == 0:
        print(c.YELLOW)
        print(ascii_box(['You have no bookmarks yet', 'Press enter to go back.'], title='No Bookmarks', padding=2, align='left'))
        print(c.RESET)       
        user_input = input()
        while user_input != '':
            clear()
            print(c.YELLOW)    
            print(ascii_box(['You have no bookmarks yet', 'Press enter to go back.'], title='No Bookmarks', padding=2, align='left'))
            print(c.RESET)    
            user_input = input('Invalid input, number only, press enter.')
        if user_input == '':
            return

    verses = []
    keys = list(bookmark.keys())  # changed: keys for dict
    for idx, key in enumerate(keys):
        value = bookmark[key]
        verses.append(f"{idx+1}. {value['book']} {value['chapter']}:{value['verse']}")
    print(c.CYAN)    
    print(ascii_box(verses, title='Bookmarks', padding=2, align='left'))
    print(c.RESET)
    user_input = input('Input bookmark number to remove, or press enter to exit: ')

    while user_input != '' and user_input.isdigit() == False:
        clear()
        print(c.CYAN)    
        print(ascii_box(verses, title='Bookmarks', padding=2, align='left'))
        print(c.RESET)
        user_input = input('Invalid input, number only, or press enter to exit: ')

    if user_input == '':
        return

    user_idx = int(user_input) - 1
    if user_idx < 0 or user_idx >= len(keys):
        print("Invalid bookmark number.")
        return

    del bookmark[keys[user_idx]]  # changed: remove by hash key
    print('Bookmark removed! Press enter to return.')

    input()

    with open('bookmark.json', 'w') as file:
        json.dump(bookmark, file, indent = 4)

# function that clears the bookmarks
def clear_bookmarks():
    try:
        with open('bookmark.json', 'r') as file:
            bookmarks = json.load(file)
    except FileNotFoundError:
        bookmarks = {}
    print(c.RED)
    print(ascii_box(['Are you sure, you want to clear the bookmarks? y/n: '], title="Clear Bookmark", padding=2, align='left'))
    print(c.RESET)    
    user = input('> ')
    while user.lower() not in 'yn':
        user = input('Invalid Input, y or n only: ')
    
    if user.lower() == 'n':
        return
    elif user.lower() == 'y':
        bookmarks.clear()
        with open('bookmark.json', 'w') as file:
            json.dump(bookmarks, file)
        clear()
        print(c.GREEN)
        print(ascii_box(['Bookmarks cleared, press enter to go back.'], title="Clear Bookmark", padding=2, align='left'))
        print(c.RESET)        
        input()

# start_bm and add_bookmark can remain mostly unchanged, but add_bookmark should use hash table as well
def add_bookmark(idx1, idx2, idx3):
    book = idx1
    chapter = int(idx2)
    verse = int(idx3)

    key = f"{book}-{chapter}-{verse}"  # changed: unique hash key
    bookmark_entry = create_bookmark([book, chapter, verse])

    try:
        with open('bookmark.json', 'r') as file:
            bookmark = json.load(file)
            if isinstance(bookmark, list):  # migrate old list to dict
                new_bookmark = {}
                for bm in bookmark:
                    k = f"{bm['book']}-{bm['chapter']}-{bm['verse']}"
                    new_bookmark[k] = bm
                bookmark = new_bookmark
    except FileNotFoundError:
        bookmark = {}

    if key in bookmark:  # check using hash key
        print('Bookmark already exists.')
    else:
        bookmark[key] = bookmark_entry  # add to dict
        with open('bookmark.json', 'w') as file:
            json.dump(bookmark, file, indent=4)
        print('Bookmark Added.')
    return input('Press enter to continue.')

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
        user = input('Your Input: ')

        while user.isdigit() == False:
            clear()
            print(c.CYAN)
            print(ascii_box(bm_menu, title="Bookmarks Menu", padding=2, align='left'))
            print(c.RESET)    
            user = input('Invalid Input. Numbers only: ')
        
        user_int = int(user)

        clear()

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
