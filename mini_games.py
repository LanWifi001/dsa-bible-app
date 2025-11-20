import json
import os
import random

from utils import ascii_box, clear
import color as c


def _print_colored_box(lines, color_code=c.RESET, **box_kwargs):
    """ ---> Utility to print ascii_box output with ANSI color wrappers.<--- """
    print(color_code)
    print(ascii_box(lines, **box_kwargs))
    print(c.RESET)


def _choices():
    """ ---> Uniform prompt used by all menus to keep navigation consistent.<--- """
    print("Press Q to return to the previous Page")
    return input("Choose a number: ")


def games_menu():
    """ ---> Entry point for all mini games displayed from the main UI.<--- """
    options = [
        "1. Verse Fill-in",
        "2. Who Said It? (coming soon)",
        "3. Story Sequence (coming soon)",
        "4. Return"
    ]

    while True:
        clear()
        _print_colored_box(options, c.CYAN, title="Mini Games", padding=2, align='left')
        choice = _choices().strip().lower()

        if choice in {'4', 'q'}:
            clear()
            return

        match choice:
            case '1':
                verse_fill_game()
            case '2':
                show_placeholder_game("Who Said It?")
            case '3':
                show_placeholder_game("Story Sequence")
            case _:
                _print_colored_box(["Invalid Input"], c.RED, title="Error", padding=2)
                input("Press Enter to continue...")


def show_placeholder_game(game_name):
    """Friendly message used for modes that are not built games yet..."""
    clear()
    lines = [f"{game_name} is coming soon!", "Check back after the next update."]
    _print_colored_box(lines, c.MAGENTA, title="Work in Progress", padding=2, align='center')
    input("Press Enter to return to the Games menu...")


def verse_fill_game():
    """ ---> Run the Verse Fill-in game loop until user exits or runs out of prompts.<--- """
    prompts = _load_verse_fill_prompts()
    if not prompts:
        return

    random.shuffle(prompts)
    rounds_played = 0
    score = 0
    exit_requested = False

    for entry in prompts:
        answers = entry.get("answers", [])
        if not answers:
            continue

        attempts_remaining = 2
        while True:
            clear()
            lines = [
                entry.get("text", ""),
                "",
                f"Blank count: {len(answers)} | Reference: {entry.get('reference', 'Unknown')}"
            ]

            hint = entry.get("hint")
            if hint:
                lines.append(f"Hint: {hint}")

            lines.extend([
                "",
                "Enter missing words separated by commas.",
                "Type 'S' to skip or 'Q' to quit the game."
            ])

            _print_colored_box(lines, c.BRIGHT_CYAN, title="Verse Fill-in", padding=2, align='left')
            user_input = input("> ").strip()

            if not user_input:
                continue

            lowered = user_input.lower()
            if lowered == 'q':
                exit_requested = True
                break
            if lowered == 's':
                _reveal_answers(entry, answers, skipped=True)
                rounds_played += 1
                break

            player_answers = _parse_player_answers(user_input, len(answers))
            if len(player_answers) != len(answers):
                _print_colored_box([f"Please enter {len(answers)} answer(s)."], c.YELLOW, title="Try Again", padding=2)
                input("Press Enter to retry...")
                continue

            player_normalized_answers = [_normalize_answer(g) for g in player_answers]
            norm_answers = [_normalize_answer(ans) for ans in answers]

            if player_normalized_answers == norm_answers:
                score += 1
                rounds_played += 1
                clear()
                _print_colored_box([
                    "Correct!",
                    f"Reference: {entry.get('reference', 'Unknown')}"
                ], c.GREEN, title="Great Job!", padding=2, align='center')
                input("Press Enter to continue...")
                break

            attempts_remaining -= 1
            if attempts_remaining > 0:
                _print_colored_box(["Not quite. Try again!"], c.BRIGHT_YELLOW, title="Incorrect", padding=2)
                input("Press Enter to retry...")
            else:
                rounds_played += 1
                _reveal_answers(entry, answers)
                break

        if exit_requested:
            break

    _show_game_summary("Verse Fill-in", rounds_played, score)


def _load_verse_fill_prompts():
    """ ---> Load verse prompts from JSON and surface friendly errors if unavailable.<--- """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verse_fill.json")
    try:
        with open(file_path, encoding='utf-8') as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("verse_fill.json must contain a list of prompts.")
        return data
    except FileNotFoundError:
        error_msg = "Missing file: verse_fill.json."
    except json.JSONDecodeError as exc:
        error_msg = f"Could not parse verse_fill.json: {exc}"
    except ValueError as exc:
        error_msg = str(exc)
    except Exception as exc:
        error_msg = f"Unexpected error: {exc}"

    clear()
    _print_colored_box([error_msg], c.RED, title="Verse Fill-in", padding=2)
    input("Press Enter to return...")
    return []


def _reveal_answers(entry, answers, skipped=False):
    """ ---> Show the correct answers after a skip or failed attempt.<--- """
    clear()
    prefix = "Skipped." if skipped else "Out of attempts."
    lines = [
        f"{prefix} Correct answers: {', '.join(answers)}",
        f"Reference: {entry.get('reference', 'Unknown')}"
    ]
    color = c.CYAN if skipped else c.BRIGHT_RED
    _print_colored_box(lines, color, title="Answer", padding=2, align='left')
    input("Press Enter to continue...")


def _parse_player_answers(raw_input, expected_count):
    """ ---> Normalize user answers (comma or whitespace separated) into a list.<--- """
    if ',' in raw_input:
        parts = [segment.strip() for segment in raw_input.split(',') if segment.strip()]
    else:
        raw_input = raw_input.strip()
        if expected_count == 1:
            parts = [raw_input] if raw_input else []
        else:
            parts = [segment for segment in raw_input.split() if segment]
    return parts


def _normalize_answer(value):
    """ ---> Lowercase and trim so spaces/upper or lowercase don't matter.<--- """
    return value.strip().lower()


def _show_game_summary(title, rounds_played, score):
    """ ---> Display end-of-session stats for the game.<--- """
    clear()
    lines = [
        f"Rounds played: {rounds_played}",
        f"Correct answers: {score}",
    ]

    if rounds_played:
        accuracy = (score / rounds_played) * 100
        lines.append(f"Accuracy: {accuracy:.0f}%")
    else:
        lines.append("Tip: Finish at least one round to build your streak.")

    _print_colored_box(lines, c.BRIGHT_BLUE, title=f"{title} Summary", padding=2, align='center')
    input("Press Enter to return to the Games menu...")