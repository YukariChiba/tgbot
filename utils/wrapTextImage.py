from PIL.ImageFont import FreeTypeFont
import re


def fitText(
    base,
    font: FreeTypeFont,
    text: str,
    max_width: int,
    max_height: int,
    spacing: int = 4,
):
    words = re.compile("[a-zA-Z0-9_]+|.").findall(text)
    line_height = font.size
    if line_height > max_height:
        # The line height is already too big
        return None

    lines: list[str] = [""]
    curr_line_width = 0

    for word in words:
        #new_line_width = font.getlength(f"{lines[-1]}{word}")
        new_line_width, _ = base.getsize(f"{lines[-1]}{word}", font=font)

        if new_line_width > max_width:
            # Word is too long to fit on the current line
            #word_width = font.getlength(word)
            word_width, _ = base.getsize(word, font=font)

            if word.encode().isalpha():
                post_word = word
                while new_line_width > max_width:
                    cutpoint = search_cut(
                        base, font, lines[-1], post_word, max_width, len(post_word), len(post_word))
                    if cutpoint < 3:
                        cutpoint = 0
                    if cutpoint == 0:
                        pre_word = post_word[:cutpoint]
                    else:
                        pre_word = post_word[:cutpoint] + "-"
                    post_word = post_word[cutpoint:]
                    lines[-1] = f"{lines[-1]}{pre_word}"
                    word_width, _ = base.getsize(pre_word, font=font)
                    curr_line_width = word_width
                    new_line_width, _ = base.getsize(f"{post_word}", font=font)
                    if new_line_width > max_width:
                        lines.append("")
                if post_word != "":
                    lines.append(post_word)
            else:
                # Put the word on the next line
                lines.append(word)
                curr_line_width = word_width

            new_text_height = len(lines) * (line_height + spacing)

            if new_text_height > max_height:
                # Word is longer than max_width, and
                # adding a new line would make the text too tall
                print(
                    "Word is longer than max_width, adding a new line would make the text too tall")
                return None
        else:
            # Put the word on the current line
            lines[-1] = f"{lines[-1]}{word}"
            curr_line_width = new_line_width

    return "\n".join(lines)


def search_cut(base, font, line, text, maxw, pos, prev_pos):
    if pos == 0:
        return pos
    w, _ = base.getsize(f'{line}{text[:pos]}', font=font)
    if w > maxw:
        if (pos - prev_pos == 1):
            return prev_pos
        return search_cut(base, font, line, text, maxw, pos//2, pos)
    elif w < maxw:
        if (pos == prev_pos):
            return pos
        if w == len(text):
            return pos
        return search_cut(base, font, line, text, maxw, (pos + prev_pos)//2, pos)
    else:
        return pos
