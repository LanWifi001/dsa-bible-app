import textwrap
import shutil
import os

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