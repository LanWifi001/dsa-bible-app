import KJV as kjv
import time as t
from utils import ascii_box, clear

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
    print(ascii_box(['Search for a word: '], title = 'Verse of the Day', padding=2, align='center'))
    user = input('> ')
    print()

    matches = search_bible(user, kjv.bible)

    # if len(matches) == 0:
    #     print('No matches found.')
    clear()
    print(f'{len(matches)} matches found.')
    for i in matches:
        verse = i.split('+')
        print(ascii_box(verse, padding=2, align='center'))
        t.sleep(0.18)
        print()
    
    user = input('Press enter to return.')
    while user != '':
        user = input('Press enter only.')
    if user == '':
        return
