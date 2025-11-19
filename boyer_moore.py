import KJV as kjv
import time as t
from utils import ascii_box, clear
import search_history as sh
import color as c

def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)

    if m == 0:
        return 0

    # --------------------------
    # 1. Build bad character table
    # --------------------------
    bad_char = {}
    for i in range(m - 1):
        bad_char[pattern[i]] = m - 1 - i

    # --------------------------
    # 2. Good suffix table
    # --------------------------
    good_suffix = [0] * (m + 1)
    border_pos = [0] * (m + 1)

    i = m
    j = m + 1
    border_pos[i] = j

    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if good_suffix[j] == 0:
                good_suffix[j] = j - i
            j = border_pos[j]
        i -= 1
        j -= 1
        border_pos[i] = j

    j = border_pos[0]
    for i in range(m + 1):
        if good_suffix[i] == 0:
            good_suffix[i] = j
        if i == j:
            j = border_pos[j]

    # --------------------------
    # 3. Search phase
    # --------------------------
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1

        if j < 0:
            return i  # match found

        skip_bad = bad_char.get(text[i + j], m)
        skip_good = good_suffix[j + 1]
        i += max(skip_bad, skip_good)

    return -1

def search_bible(pattern, bible):
    results = []

    for book in bible["books"]:
        book_name = book["name"]

        for chapter in book["chapters"]:
            chapter_num = chapter["chapter"]

            for verse in chapter["verses"]:
                verse_num = verse["verse"]
                verse_text = verse["text"]

                # Boyer-Moore search
                pos = boyer_moore(verse_text.lower(), pattern.lower())

                if pos != -1:
                    results.append(f"{book_name} {chapter_num}:{verse_num}+{verse_text}")

    return results

def run_boyer_moore():
    while True:
        clear()
        print(c.CYAN)
        print(ascii_box(['1. Search for a word', '2. View Search History', '3. Clear Search History', '4. Back'], title = 'Word Search', padding=2, align='left'))
        print(c.RESET)    

        user = input('Enter the number: ')
        print()

        while user.isdigit() == False:
            clear()
            print(c.CYAN)
            print(ascii_box(['1. Search for a word', '2. View Search History', '3. Clear Search History', '4. Back'], title = 'Word Search', padding=2, align='left'))
            print(c.RESET)   
            user = input('Invalid input. Number only: ')

        user_int = int(user)

        match user_int:
            case 1:
                clear()
                print(c.CYAN)
                print(ascii_box(['Search for a word.'], title = 'Word Search', padding=2, align='left'))
                print(c.RESET)
                user_search = input('> ')
                            
                matches = search_bible(user_search, kjv.bible)

                results = len(matches)

                # if len(matches) == 0:
                #     print('No matches found.')
                clear()
                sh.add_to_history(user_search, results)
                print(c.CYAN)
                print(ascii_box([f'{results} matches found.'], title = 'Matches', padding=2, align='left'))
                print(c.RESET)
                view_results(user_search, matches, results)
            case 2:
                history()
            case 3:
                sh.clear_history()
            case 4:
                return
            case _:
                clear()
                print(c.CYAN)
                print(ascii_box(['1. Search for a word', '2. View Search History', '3. Clear Search History', '4. Back'], title = 'Word Search', padding=2, align='left'))
                print(c.RESET)    
                print('Invalid Input. Only pick from the choices: ')

def view_results(user_search, matches, results): 
    counts = 0
    print('First 50 results.')
    for i in matches:
        if counts == 50:
            break
        verse = i.split('+')
        highlight = ascii_box([verse[0], verse[1]], padding=2, align='center')
        box_color = highlight.replace(user_search, f'{c.BG_BRIGHT_YELLOW}{user_search}{c.RESET}') 
        print(box_color)
        t.sleep(0.05)
        counts += 1
        print()
    print('Press enter to view all results, or "q" to go back.')
    user = input('> ')
    while user != '' and user.lower() != 'q':
        clear()
        print(c.CYAN)
        print(ascii_box([f'{results} matches found.'], title = 'Matches', padding=2, align='left'))
        print(c.RESET)
        print('Invalid Input. Press enter or "q" only.')
        user = input('> ')

    if user == '':
        clear()
        print(c.CYAN)
        print(ascii_box([f'{results} matches found.'], title = 'Matches', padding=2, align='left'))
        print(c.RESET)
        for i in matches:
            verse = i.split('+')
            highlight = ascii_box([verse[0], verse[1]], padding=2, align='center')
            box_color = highlight.replace(user_search, f'{c.BG_BRIGHT_YELLOW}{user_search}{c.RESET}') 
            print(box_color)
            t.sleep(0.05)
            print()
        
        user = input('Press enter to return.')
        while user != '':
            user = input('Press enter only.')
        if user == '':
            return
    elif user == 'q':
        return

def history():  
    clear()
    sh.show_search_history()
    user = input('Press enter to return.')
    while user != '':
        user = input('Press enter only.')
    if user == '':
        return