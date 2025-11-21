import textwrap            # Wrap long strings for terminal display
import shutil              # Get terminal size to adjust formatting
import os                  # Clear terminal or handle file paths

# ---------------------------------------
# Function: ascii_box
# Description: Create a text box with optional title, padding, alignment, and borders
# ---------------------------------------
def ascii_box(lines, title=None, padding=1, align='left', max_width=None, border_chars=None, save_path=None):
    
    # Attempt to detect terminal width, fallback to 80 if not possible
    try:
        term_width = shutil.get_terminal_size().columns
    except Exception:
        term_width = 80

    # Determine max width for text inside the box
    if max_width is None:
        max_width = max(20, term_width - 6)  # Leave space for borders

    # Wrap each line to the max_width
    wrapped_lines = []
    for raw in lines:
        if raw is None:
            raw = ''  # Treat None as empty string
        wrapped = textwrap.wrap(str(raw), width=max_width) or ['']  # Wrap line, ensure at least one line
        wrapped_lines.extend(wrapped)

    # Include title in width calculation if present
    candidates = wrapped_lines[:] if wrapped_lines else ['']
    if title:
        candidates.append(title)

    inner_width = max(len(s) for s in candidates)  # Determine widest content
    box_inner = inner_width + padding * 2          # Add padding spaces on left and right

    # Ensure box fits inside terminal width
    if box_inner + 2 > term_width:  # +2 for border characters
        box_inner = max(10, term_width - 2)       # Shrink box if too wide
        inner_width = box_inner - padding * 2

    # Default Unicode borders
    if border_chars is None:
        tl, tr, bl, br, h, v = '╔', '╗', '╚', '╝', '═', '║'
    else:
        tl, tr, bl, br, h, v = border_chars  # Custom border characters

    # Construct top and bottom borders
    top = tl + (h * box_inner) + tr
    bottom = bl + (h * box_inner) + br

    out_lines = [top]  # Start output with top border

    # Add title if provided
    if title:
        title_text = title[:box_inner]  # Truncate title if too long
        out_lines.append(v + title_text.center(box_inner) + v)  # Centered title
        out_lines.append('╠' + (h * box_inner) + '╣')           # Separator under title

    # Add wrapped content lines
    for l in wrapped_lines:
        if len(l) > inner_width:
            l = l[:inner_width]  # Truncate if somehow still too long

        # Align text according to parameter
        if align == 'left':
            content = l.ljust(inner_width)
        elif align == 'center':
            content = l.center(inner_width)
        else:
            content = l.rjust(inner_width)

        # Construct final line with vertical borders and padding
        line = v + (' ' * padding) + content + (' ' * padding) + v
        out_lines.append(line)

    # Add bottom border
    out_lines.append(bottom)

    # Join all lines into a single string
    result = "\n".join(out_lines)

    # Optionally save box to file
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(result)
        except Exception:
            pass  # Ignore errors if file can't be written

    return result  # Return the box as string

# ---------------------------------------
# Function: clear
# Description: Clears the terminal screen
# ---------------------------------------
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')  # Windows vs Linux/Mac
