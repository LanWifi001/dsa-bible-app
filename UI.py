import bookmark as b       # Access bookmark functionality
from utils import ascii_box, clear  # Format UI and clear screen
import boyer_moore as bm  # Search functionality using Boyer-Moore algorithm
from KJV import bible      # Complete Bible data
import verse_of_the_day as votd  # Fetch daily verse
import color as c          # Terminal colors
import time as t           # Delays for UI animations
from mini_games import games_menu  # Access mini-games menu

# ---------------------------------------
# Function: choices
# Description: Prompt user to choose a number or press Q to go back
# ---------------------------------------
def choices():
    print("Press Q to go back")  # Inform user they can quit
    return input("Choose a number: ").strip()  # Return stripped user input

# ---------------------------------------
# Function: main
# Description: Display main menu and route user choices
# ---------------------------------------
def main():
    clear()  # Clear screen
    menu_lines = ["1. Books", 
                  "2. Bookmarks",
                  "3. Search Verse",
                  "4. Search Text",
                  "5. Games",
                  "6. Exit"
                  ]

    while True:
        print(c.YELLOW)
        print(ascii_box(votd.get_verse_of_the_day(), title = 'Verse of the Day', padding=2, align='center'))  # Show Verse of the Day
        print(c.CYAN)
        print(ascii_box(menu_lines, title="Mini Bible", padding=2, align='left'))  # Display main menu
        print(c.RESET)

        choice = input("Choose a number: ").strip()  # Get user choice
        clear()  # Clear screen before handling choice
        
        match choice:  # Route choice
            case '1':
                choose_old_or_new()  # Go to Old/New Testament selection
                clear()
            case '2': 
                b.start_bm()  # Open bookmarks menu
                clear()
            case '3':
                search_verse()  # Search a specific verse
                clear()
            case '4':
                bm.run_boyer_moore()  # Search text using Boyer-Moore
                clear()
            case '5':
                games_menu()  # Open mini-games menu
                clear()
            case '6':
                main_screen()  # Go back to splash screen
                return
            case _:
                clear()
                print(c.RED)
                print(ascii_box([f"Invalid Input"], title="Error", padding=2))  # Invalid input message
                print(c.RESET)

# ---------------------------------------
# Function: choose_old_or_new
# Description: Allow user to select Old or New Testament
# ---------------------------------------
def choose_old_or_new():
    books_list = [book['name'] for book in bible['books']]  # Extract all book names
    old = books_list[:39]  # Old Testament books
    new = books_list[39:]  # New Testament books

    while True:
        clear()
        print(c.CYAN)
        print(ascii_box(['1. Old Testament', '2. New Testament', '3. Return'], title='Select Testament', padding=2, align='left'))  # Show Testament menu
        print(c.RESET)
        choice = input('Choose a number: ').strip()  # Get user input

        while choice.isdigit == False:  # Validate numeric input
            print(c.CYAN)
            print(ascii_box(['1. Old Testament', '2. New Testament', '3. Return'], title='Select Testament', padding=2, align='left'))
            print(c.RESET)
            choice = input(c.RED, 'Invalid Input.', c.RESET).strip()  # Prompt again

        match choice:
            case '1':
                clear()
                books_menu(old, 'Old Testament')  # Open Old Testament books
            case '2':
                clear()
                books_menu(new, 'New Testament')  # Open New Testament books
            case '3':
                clear()
                return  # Return to main menu
            case _:
                print(c.RED, 'Invalid Input.', c.RESET)

# ---------------------------------------
# Function: books_menu
# Description: Display books in paginated menu
# ---------------------------------------
def books_menu(books_list, book_title):
    page = 0  # Current page index
    per_page = 20  # Books per page

    while True:
        start_idx = page * per_page
        end_idx = start_idx + per_page
        page_books = books_list[start_idx:end_idx]  # Slice current page books

        menu_lines = []  # Lines to display
        actions = {}  # Map number to action
        num = 1  # Local numbering for menu

        # Add books to menu
        for book in page_books:
            menu_lines.append(f"{num}. {book}")
            actions[num] = ('book', book)  # Action: open book
            num += 1

        # Pagination controls
        if end_idx < len(books_list):
            clear()
            menu_lines.append(f"{num}. Next Page")
            actions[num] = ('next', None)
            num += 1
        if page > 0:
            clear()
            menu_lines.append(f"{num}. Previous Page")
            actions[num] = ('prev', None)
            num += 1

        clear()
        print(c.CYAN)
        print(ascii_box(menu_lines, title=book_title, padding=2, align='left'))  # Show menu
        print(c.RESET)    

        choice = choices()  # Get user choice
        input1 = choice.lower()

        if input1 == 'q':  # Return to main menu
            clear()
            return main()

        try:
            choice_num = int(choice)  # Convert to integer
        except ValueError:
            print(c.RED)
            print(ascii_box([f"Invalid Input"], title="Error", padding=2))
            print(c.RESET)
            continue

        if choice_num not in actions:  # Validate number
            print(c.RED)
            print(ascii_box([f"Invalid Input"], title="Error", padding=2))
            print(c.RESET)    
            continue

        action, payload = actions[choice_num]

        if action == 'book':
            clear()
            chapter_menu(payload)  # Show chapters for selected book
            continue
        elif action == 'next':
            page += 1  # Go to next page
            continue
        elif action == 'prev':
            page = max(0, page - 1)  # Go to previous page
            continue

# ---------------------------------------
# Function: chapter_menu
# Description: Display chapters for selected book
# ---------------------------------------
def chapter_menu(book_name):
    book_data = None
    # Find book in Bible data
    for book in bible['books']:
        if book['name'] == book_name:
            book_data = book
            break

    if book_data is None:
        print(c.RED)
        print(ascii_box([f"Book '{book_name}' not found in database"], title="Error", padding=2))
        print(c.RESET)
        return

    book_chapters = {str(ch['chapter']): ch['verses'] for ch in book_data['chapters']}  # Map chapter number to verses
    chapter_list = sorted(book_chapters.keys(), key=lambda x: int(x))  # Sort chapter numbers

    page = 0  # Pagination
    per_page = 10

    while True:
        start_idx = page * per_page
        end_idx = start_idx + per_page
        page_chapters = chapter_list[start_idx:end_idx]  # Chapters on current page

        menu_lines = []
        actions = {}
        num = 1

        # Add chapters to menu
        for ch in page_chapters:
            menu_lines.append(f"{num}. Chapter {ch}")
            actions[num] = ('chapter', ch)
            num += 1

        # Pagination controls
        if end_idx < len(chapter_list):
            menu_lines.append(f"{num}. Next Page")
            actions[num] = ('next', None)
            num += 1
        if page > 0:
            menu_lines.append(f"{num}. Previous Page")
            actions[num] = ('prev', None)
            num += 1

        print(c.CYAN)
        print(ascii_box(menu_lines, title=f"{book_name} - Chapters (Page {page+1})", padding=2, align='left'))
        print(c.RESET)

        choice = choices()
        input1 = choice.lower()
        clear()

        if input1 == 'q':  # Return to books menu
            return 

        try:
            choice_num = int(choice)
        except ValueError:
            print(c.RED)
            print(ascii_box([f"Invalid Input"], title="Error", padding=2))
            print(c.RESET)
            continue

        if choice_num not in actions:
            print(c.RED)
            print(ascii_box([f"Invalid Input"], title="Error", padding=2))
            print(c.RESET)
            continue

        action, payload = actions[choice_num]
        if action == 'chapter':
            verse_menu(book_name, payload, book_chapters[payload])  # Show verses for selected chapter
            continue
        elif action == 'next':
            page += 1
            continue
        elif action == 'prev':
            page = max(0, page - 1)
            continue

# ---------------------------------------
# Function: verse_menu
# Description: Display verses from selected chapter and navigate them
# ---------------------------------------
def verse_menu(book_name, chapter_num, verses):
    verse_dict = {str(v['verse']): v['text'] for v in verses}  # Map verse numbers to text
    verse_list = sorted(verse_dict.keys(), key=lambda x: int(x))  # Sorted verse numbers

    print(c.CYAN)
    print(ascii_box([f"Available verses: {', '.join(verse_list)}"], title=f"{book_name} Chapter {chapter_num}", padding=2, align='center'))
    print(c.RESET)

    # Prompt user to start from a verse
    while True:
        choice = choices()
        input1 = choice.lower()
        if input1 in verse_list:
            current_verse_idx = verse_list.index(choice)  # Index for navigation
            break
        elif input1 == 'q':
            clear()
            return
        else:
            clear()
            print(c.CYAN)
            print(ascii_box([f"Available verses: {', '.join(verse_list)}"], title=f"{book_name} Chapter {chapter_num}", padding=2, align='center'))
            print(c.RESET)
            print(c.RED)
            print(ascii_box([f"Invalid input"], title="Error", padding=2))
            print(c.RESET)

    # Verse navigation loop
    while True:
        current_verse = verse_list[current_verse_idx]
        clear()
        print(c.CYAN)
        print(ascii_box([verse_dict[current_verse]], title=f"{book_name} Chapter {chapter_num} Verse {current_verse}", padding=2, align='center'))
        print(c.RESET)

        # Navigation instructions
        nav_info = ["Press Enter for next verse", "Press Q to return to chapters", "Press B to Bookmark"]
        if current_verse_idx > 0:
            nav_info.insert(0, "Press P for previous verse")
        nav_text = " | ".join(nav_info)

        user_input = input(nav_text + "\n> ").strip().lower()

        if user_input == '' or user_input == 'enter':  # Next verse
            if current_verse_idx < len(verse_list) - 1:
                current_verse_idx += 1
            else:
                clear()
                print(ascii_box(["No more verses in this chapter"], title="End of Chapter", padding=2))
                input("Press Enter to return...").strip()
                clear()
                return chapter_menu(book_name)
        elif user_input == 'p':  # Previous verse
            if current_verse_idx > 0:
                current_verse_idx -= 1
        elif user_input == 'q':  # Back to chapter menu
            clear()
            return
        elif user_input == 'b':  # Bookmark verse
            user = b.add_bookmark(book_name, chapter_num, current_verse)
            while user != '':
                user = input('Invalid Input.').strip()
            if user == '':
                continue

# ---------------------------------------
# Function: verses_of_the_day
# Description: Display verse of the day
# ---------------------------------------
def verses_of_the_day():
    clear()
    print(c.YELLOW)
    print(ascii_box(votd.get_verse_of_the_day(), title='Verse of the Day', padding=2, align='center'))
    print(c.RESET)
    choice = input("Press Enter to continue...").strip()

    while True:
        if choice == '':
            return

# ---------------------------------------
# Function: loading_screen
# Description: Show loading animation before main menu
# ---------------------------------------
def loading_screen():
    clear()
    print(c.CYAN)
    print(ascii_box(["Loading Mini Bible..."], padding=2, align='center'))
    print(c.GREEN)

    loading = '██████████████████████████████'  # Loading bar
    for bar in loading:
        print(bar, end='', flush=True)  # Print loading animation
        t.sleep(0.02)
    print(c.RESET)
    print()

    choice = input ("Press Enter to continue...").strip()
    if choice == '':
        main()

# ---------------------------------------
# Function: main_screen
# Description: Splash screen with ASCII art
# ---------------------------------------
def main_screen():
    clear()
    print(c.BRIGHT_CYAN)
    enter = ["  _   _            _     _ _     _",
    " | |_| |__   ___  | |__ (_) |__ | | ___ ",
    " | __| '_ \ / _ \ | '_ \| | '_ \| |/ _ \\",
    " | |_| | | |  __/ | |_) | | |_) | |  __/",
    "  \__|_| |_|\___| |_.__/|_|_.__/|_|\___|"]

    print(ascii_box(enter, padding=4, align='left'))
    print(c.RESET)

    print("Press Enter to continue or type exit...")
    choice = input('> ').strip()

    while choice != '' and choice.lower() != 'exit':  # Validate input
        clear()
        print(c.BRIGHT_CYAN)
        print(ascii_box(enter, padding=4, align='left'))
        print(c.RESET)
        print('Invalid Input. Press Enter to continue or type exit...')
        choice = input('> ').strip()

    if choice == '':
        loading_screen()
    elif choice.lower() == 'exit':
        return

# ---------------------------------------
# Function: search_verse
# Description: Allows user to search a specific verse by book, chapter, verse
# ---------------------------------------
def search_verse():
    print(c.BRIGHT_CYAN)
    print(ascii_box(['Search for a verse or', 'Press enter to exit'], title='Verse Search', padding=2, align='left'))
    print(c.RESET)
    print('Enter with this format (Genesis 1 1)')

    while True:
        user = input('> ').strip()
        if user == '':
            return
        else:
            user_arr = user.split()
            while len(user_arr) != 3:  # Validate input length
                clear()
                print(c.BRIGHT_CYAN)
                print(ascii_box(['Search for a verse or', 'Press enter to exit'], title='Verse Search', padding=2, align='left'))
                print(c.RESET)
                print('Invalid Input! Enter with this format (Genesis 1 1)')
                user = input('> ').strip()
                user_arr = user.split()

            # Extract book, chapter, verse
            book = user_arr[0]
            chapter = int(user_arr[1])
            verse = int(user_arr[2])

            # Search for verse in Bible
            for i in bible['books']:
                if i['name'] == book:
                    for j in i['chapters']:
                        if j['chapter'] == chapter:
                            for k in j['verses']:
                                if k['verse'] == verse:
                                    clear()
                                    print(c.BRIGHT_CYAN)
                                    print(ascii_box([k['text']], title=f'{book} {chapter}:{verse}', padding=2, align='left'))
                                    print(c.RESET)
                                    user = input('Press enter to go back.').strip()
                                    while user != '':
                                        user = input('Invalid Input. Press enter only.').strip()
                                    if user == '':
                                        clear()
                                        return
            else:
                clear()
                print(c.BRIGHT_CYAN)
                print(ascii_box(['Verse not found.'], title='Verse Search', padding=2, align='left'))
                print(c.RESET)
                user = input('Press enter to go back.').strip()
                while user != '':
                    user = input('Invalid Input. Press enter only.').strip()
                if user == '':
                    clear()
                    return
