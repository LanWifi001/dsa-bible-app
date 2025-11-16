import textwrap
import shutil
import os
import json


def ascii_box(lines, title=None, padding=1, align='left', max_width=None, border_chars=None, save_path=None):

    try:
        term_width = shutil.get_terminal_size().columns
    except Exception:
        term_width = 80

    # Choose a sane default max width inside the terminal
    if max_width is None:
        max_width = max(20, term_width - 6)

    # Wrap input lines to the max_width
    wrapped_lines = []
    for raw in lines:
        if raw is None:
            raw = ''
        wrapped = textwrap.wrap(str(raw), width=max_width) or ['']
        wrapped_lines.extend(wrapped)

    # Include title in width calculation if present
    candidates = wrapped_lines[:] if wrapped_lines else ['']
    if title:
        candidates.append(title)

    inner_width = max(len(s) for s in candidates)
    box_inner = inner_width + padding * 2

    # Ensure box fits terminal
    if box_inner + 2 > term_width:
        # shrink inner to fit
        box_inner = max(10, term_width - 2)
        inner_width = box_inner - padding * 2

    # Default Unicode borders
    if border_chars is None:
        tl, tr, bl, br, h, v = '╔', '╗', '╚', '╝', '═', '║'
    else:
        tl, tr, bl, br, h, v = border_chars

    top = tl + (h * box_inner) + tr
    bottom = bl + (h * box_inner) + br

    out_lines = [top]

    if title:
        title_text = title[:box_inner]
        out_lines.append(v + title_text.center(box_inner) + v)
        out_lines.append('╠' + (h * box_inner) + '╣')

    for l in wrapped_lines:
        if len(l) > inner_width:
            # truncate if needed (shouldn't happen because we wrapped)
            l = l[:inner_width]

        if align == 'left':
            content = l.ljust(inner_width)
        elif align == 'center':
            content = l.center(inner_width)
        else:
            content = l.rjust(inner_width)

        line = v + (' ' * padding) + content + (' ' * padding) + v
        out_lines.append(line)

    out_lines.append(bottom)

    result = "\n".join(out_lines)

    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(result)
        except Exception:
            pass

    return result

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        with open('Books.json', 'r', encoding='utf-8') as f:
            books_list = json.load(f)
    except FileNotFoundError:
        print("Error: Books.json not found")
        return
    

    menu_lines = ["1. Books", 
                  "2. Bookmarks (walang laman)",
                  "3. Search (walang laman)",
                  "4. Exit"
                  ]
    print(ascii_box(menu_lines, title="Mini Bible", padding=2, align='left'))

    verses_of_the_day()

    while True:


        choices = input("Choose a number1: ")
        clear()
        
        match choices:
            case '1':
                books_menu(books_list)

            # case '':
            #     print(ascii_box(["PLACEHOLDER"], title="Bookmarks", padding=2))
            #     break
            # case '':  
            #     print(ascii_box(["Search: "], title="Search", padding=2))
            #     break
            case _:
                print(ascii_box([f"Invalid choice: {choices}"], title="Error", padding=2))

def books_menu(books_list):
    """Display list of books and allow user to select one"""
    # Show books in chunks of 10 for readability; implement proper pagination
    page = 0
    per_page = 10
    while True:
        start_idx = page * per_page
        end_idx = start_idx + per_page
        page_books = books_list[start_idx:end_idx]
        choice1 = ''

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
            menu_lines.append(f"{num}. Next Page")
            actions[num] = ('next', None)
            num += 1
        if page > 0:
            menu_lines.append(f"{num}. Previous Page")
            actions[num] = ('prev', None)
            num += 1
            # menu_lines.append(f"{num}. Back to Main Menu")
            # actions[num] = ('back', None)
            # num += 1

        print(ascii_box(menu_lines, title=f"Books (Page {page+1})", padding=2, align='left'))

        choice = input("Choose a book (or press Enter to go back): ").strip()
        clear()

        # Empty input -> go back to main menu
        if choice == '':
            main()
            return

        try:
            choice_num = int(choice)
        except ValueError:
            print(ascii_box([f"Invalid choice: {choice}"], title="Error", padding=2))
            continue

        if choice_num not in actions:
            print(ascii_box([f"Invalid choice: {choice_num}"], title="Error", padding=2))
            continue

        action, payload = actions[choice_num]
        if action == 'book':
            # Show chapters for the selected book. When chapter_menu returns
            chapter_menu(payload)
            continue
        elif action == 'next':
            page += 1
            continue
        elif action == 'prev':
            page = max(0, page - 1)
            continue
        elif action == 'back':
            return

def chapter_menu(book_name):
    """Display chapters from a selected book and load verses from JSON"""
    try:
        with open('KJV_bible.json', 'r', encoding='utf-8') as f:
            bible_data = json.load(f)
    except FileNotFoundError:
        print(ascii_box(["Error: KJV_bible.json not found"], title="Error", padding=2))
        return
    
    # Get chapters for the selected book
    if book_name not in bible_data:
        print(ascii_box([f"Book '{book_name}' not found in database"], title="Error", padding=2))
        return
    
    book_chapters = bible_data[book_name]
    chapter_list = sorted(book_chapters.keys(), key=lambda x: int(x))
    
    # Display chapters with pagination
    page = 0
    per_page = 10
    while True:
        start_idx = page * per_page
        end_idx = start_idx + per_page
        page_chapters = chapter_list[start_idx:end_idx]

        menu_lines = []
        # actions maps displayed integer -> ('type', payload)
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

        print(ascii_box(menu_lines, title=f"{book_name} - Chapters (Page {page+1})", padding=2, align='left'))

        chapter_choice = input("Choose a chapter (or press Enter to go back): ").strip()
        clear()

        # Empty input -> go back to books menu (return to caller)
        if chapter_choice == '':
            return

        try:
            choice_num = int(chapter_choice)
        except ValueError:
            print(ascii_box([f"Invalid choice: {chapter_choice}"], title="Error", padding=2))
            continue

        if choice_num not in actions:
            print(ascii_box([f"Invalid choice: {choice_num}"], title="Error", padding=2))
            continue

        action, payload = actions[choice_num]
        if action == 'chapter':
            verse_menu(book_name, payload, book_chapters[payload])
            return
        elif action == 'next':
            page += 1
            continue
        elif action == 'prev':
            page = max(0, page - 1)
            continue
        elif action == 'back':
            return


def verse_menu(book_name, chapter_num, verses):
    """Display a single verse from a selected chapter."""
    verse_list = sorted(verses.keys(), key=lambda x: int(x))
    print(ascii_box([f"Available verses: {', '.join(verse_list)}"],
                    title=f"{book_name} Chapter {chapter_num}", padding=2, align='left'))

    while True:
        choice = input("Enter verse number to read: ")
        if choice in verses:
            clear()
            print(ascii_box([verses[choice]],
                            title=f"{book_name} Chapter {chapter_num} Verse {choice}", padding=2, align='left'))
            input("Press Enter to continue to the next verse...")
            clear()
            break
        else:
            print("Invalid verse number. Try again.")


def verses_of_the_day():
    print("Placeholder for Verses of the Day functionality")

if __name__ == '__main__':
    main()