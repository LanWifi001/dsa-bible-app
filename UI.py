import bookmark as b
from utils import ascii_box, clear
import boyer_moore as bm
from KJV import bible
import verse_of_the_day as votd
import color as c
import time as t
from mini_games import games_menu

def choices():
    print("Press Q to go back")
    return input("Choose a number: ")

def main():
    clear()
    menu_lines = ["1. Books", 
                  "2. Bookmarks",
                  "3. Search",
                  "4. Games",
                  "5. Exit"
                  ]

    while True:
        print(c.YELLOW)
        print(ascii_box(votd.votd, title = 'Verse of the Day', padding=2, align='center'))
        print(c.CYAN)
        print(ascii_box(menu_lines, title="Mini Bible", padding=2, align='left'))
        print(c.RESET)

        choice = input("Choose a number: ")
        clear()
        
        match choice:
            case '1':
                choose_old_or_new()
                clear()

            case '2': 
                b.start_bm()
                clear()

            case '3':
                bm.run_boyer_moore()
                clear()

            case '4':
                games_menu()
                clear()

            case '5':
                main_screen()
                return
            
            case _:
                clear()
                print(c.RED)
                print(ascii_box([f"Invalid Input"], title="Error", padding=2))
                print(c.RESET)
                # print("Press Q to return to the previous Page |")
                # input1 = choice.lower()
                # if input1 == 'q':
                #     clear()
                #     return main()
    # return

def choose_old_or_new():
    # Extract book names from the KJV.py bible dictionary
    books_list = [book['name'] for book in bible['books']]

    old = books_list[:39]
    new = books_list[39:]
    while True:
        clear()
        print(c.CYAN)
        print(ascii_box(['1. Old Testament', '2. New Testament', '3. Return'], title='Select Testament', padding=2, align='left'))
        print(c.RESET)
        choice = input('Choose a number: ')

        while choice.isdigit == False:
            print(c.CYAN)
            print(ascii_box(['1. Old Testament', '2. New Testament', '3. Return'], title='Select Testament', padding=2, align='left'))
            print(c.RESET)
            choice = input(c.RED, 'Invalid Input.', c.RESET)

        match choice:
            case '1':
                clear()
                books_menu(old, 'Old Testament')
            case '2':
                clear()
                books_menu(new, 'New Testament')
            case '3':
                clear()
                return
            case _:
                print(c.RED, 'Invlid Input.', c.RESET)

def books_menu(books_list, book_title):
    """Display list of books and allow user to select one"""
    # Show books in chunks of 20 for readability; implement proper pagination
    page = 0
    per_page = 20
    while True:
        start_idx = page * per_page
        end_idx = start_idx + per_page
        page_books = books_list[start_idx:end_idx]

        menu_lines = []
        # actions maps displayed integer -> ('type', payload)
        actions = {}
        num = 1

        # List books for this page with local numbering 1..N
        for book in page_books:
            menu_lines.append(f"{num}. {book}")
            actions[num] = ('book', book)
            num += 1

        # Add pagination controls after the books
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
            # menu_lines.append(f"{num}. Back to Main Menu")
            # actions[num] = ('back', None)
            # num += 1

        clear()
        print(c.CYAN)
        print(ascii_box(menu_lines, title=book_title, padding=2, align='left'))
        print(c.RESET)    

        choice = choices()
        input1 = choice.lower()
        # ERROR HANDLING
        # Empty input -> go back to main menu (return to caller)
        if input1 == 'q':
            clear()
            return main()

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
        if action == 'book':
            clear()
            # Show chapters for the selected book. When chapter_menu returns
            chapter_menu(payload)
            continue
        elif action == 'next':
            page += 1
            continue
        elif action == 'prev':
            page = max(0, page - 1)
            continue
        # elif action == 'back':
        #     return

def chapter_menu(book_name):
    """Display chapters from a selected book and load verses from KJV"""
    # Find the book in the bible data
    book_data = None
    for book in bible['books']:
        if book['name'] == book_name:
            book_data = book
            break
    
    if book_data is None:
        print(c.RED)
        print(ascii_box([f"Book '{book_name}' not found in database"], title="Error", padding=2))
        print(c.RESET)
        return
    
    # Extract chapters from the book
    book_chapters = {str(ch['chapter']): ch['verses'] for ch in book_data['chapters']}
    chapter_list = sorted(book_chapters.keys(), key=lambda x: int(x))
    
    # Display chapters with pagination
    page = 0
    per_page = 10
    while True:
        start_idx = page * per_page
        end_idx = start_idx + per_page
        page_chapters = chapter_list[start_idx:end_idx]

        menu_lines = []
        actions = {}
        num = 1

        # List chapters for this page with local numbering 1..N
        for ch in page_chapters:
            menu_lines.append(f"{num}. Chapter {ch}")
            actions[num] = ('chapter', ch)
            num += 1

        # Add pagination controls after the chapters
        if end_idx < len(chapter_list):
            menu_lines.append(f"{num}. Next Page")
            actions[num] = ('next', None)
            num += 1
        if page > 0:
            menu_lines.append(f"{num}. Previous Page")
            actions[num] = ('prev', None)
            num += 1
        
        # menu_lines.append(f"{num}. Back to Books")
        # actions[num] = ('back', None)
        # num += 1

        print(c.CYAN)        
        print(ascii_box(menu_lines, title=f"{book_name} - Chapters (Page {page+1})", padding=2, align='left'))
        print(c.RESET)

        choice = choices()
        input1 = choice.lower()
        clear()

        # Empty input -> go back to books menu (return to caller)
        if input1 == 'q':
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
            verse_menu(book_name, payload, book_chapters[payload])
            continue
        elif action == 'next':
            page += 1
            continue
        elif action == 'prev':
            page = max(0, page - 1)
            continue
        # elif action == 'back':
        #     return

def verse_menu(book_name, chapter_num, verses):
    """Display verses from a selected chapter with navigation."""
    # Convert verses list to a dictionary {verse_num: text}
    verse_dict = {str(v['verse']): v['text'] for v in verses}
    verse_list = sorted(verse_dict.keys(), key=lambda x: int(x))
    
    print(c.CYAN)
    print(ascii_box([f"Available verses: {', '.join(verse_list)}"],
                    title=f"{book_name} Chapter {chapter_num}", padding=2, align='center'))
    print(c.RESET)

    # Get starting verse from user
    while True:
        choice = choices()
        input1 = choice.lower()
        if input1 in verse_list:
            current_verse_idx = verse_list.index(choice)
            break
        elif input1 == 'q':
            clear()
            return 
        # chapter_menu(book_name)
        else:
            clear()
            print(c.CYAN)
            print(ascii_box([f"Available verses: {', '.join(verse_list)}"],
                            title=f"{book_name} Chapter {chapter_num}", padding=2, align='center'))
            print(c.RESET)
            print(c.RED)            
            print(ascii_box([f"Invalid input"], title="Error", padding=2))
            print(c.RESET)

    # Navigate through verses
    while True:
        current_verse = verse_list[current_verse_idx]
        clear()
        print(c.CYAN)
        print(ascii_box([verse_dict[current_verse]],
                        title=f"{book_name} Chapter {chapter_num} Verse {current_verse}", padding=2, align='center'))
        print(c.RESET)

        # Show navigation instructions
        nav_info = ["Press Enter for next verse", "Press Q to return to chapters", "Press B to Bookmark"]
        if current_verse_idx > 0:
            nav_info.insert(0, "Press P for previous verse")
        
        nav_text = " | ".join(nav_info)
        user_input = input(nav_text + "\n> ").strip().lower()
        
        if user_input == '' or user_input == 'enter':
            # Move to next verse
            if current_verse_idx < len(verse_list) - 1:
                current_verse_idx += 1
            else:
                clear()
                print(ascii_box(["No more verses in this chapter"], title="End of Chapter", padding=2))
                input("Press Enter to return...")
                clear()
                return chapter_menu(book_name)
        elif user_input == 'p':
            # Move to previous verse
            if current_verse_idx > 0:
                current_verse_idx -= 1
        elif user_input == 'q':
            # Return to chapter selection
            clear()
            return
        elif user_input == 'b':
            user = b.add_bookmark(book_name, chapter_num, current_verse)
            while user != '':
                user = input('Invalid Input.')
            if user == '':
                continue

def verses_of_the_day():
    clear()
    print(c.YELLOW)        
    print(ascii_box(votd.get_verse_of_the_day(), title = 'Verse of the Day', padding=2, align='center'))
    print(c.RESET)    
    choice = input("Press Enter to continue...")

    while True:
        if choice == '':
            return
        # else:
        #     verses_of_the_day()

def loading_screen():
    clear()
    
    print(c.CYAN)
    print(ascii_box(["Loading Mini Bible..."], padding=2, align='center'))
    print(c.GREEN)
    loading = '██████████████████████████████'
    for bar in loading:
        print(bar, end='', flush=True)
        t.sleep(0.02)
    print(c.RESET)

    print()

    choice = input ("Press Enter to continue...")

    if choice == '':
        main()
    #     verses_of_the_day()
    # else:
    #     loading_screen()

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
    choice = input('> ')

    while choice != '' and choice.lower() != 'exit':
        clear()
        print(c.BRIGHT_CYAN)
        enter = ["  _   _            _     _ _     _",
        " | |_| |__   ___  | |__ (_) |__ | | ___ ",
        " | __| '_ \ / _ \ | '_ \| | '_ \| |/ _ \\",
        " | |_| | | |  __/ | |_) | | |_) | |  __/",
        "  \__|_| |_|\___| |_.__/|_|_.__/|_|\___|"]

        print(ascii_box(enter, padding=4, align='left'))
        print(c.RESET)
        print('Invalid Input. Press Enter to continue or type exit...')
        choice = input('> ')
    
    if choice == '':
        loading_screen()
    elif choice.lower() == 'exit':
        return
    # else:
    #     main_screen()

# run main UI
# def run_UI():
#     main_screen()