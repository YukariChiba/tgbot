from PIL.ImageFont import FreeTypeFont


def fitText(
    base,
    font: FreeTypeFont,
    text: str,
    max_width: int,
    max_height: int,
    spacing: int = 4,
):
    words = list(text)
    line_height = font.size
    if line_height > max_height:
        # The line height is already too big
        return None

    lines: list[str] = [""]
    curr_line_width = 0

    for word in words:
        if curr_line_width == 0:
            #word_width = font.getlength(word)
            word_width, _ = base.getsize(word, font=font)

            if word_width > max_width:
                # Word is longer than max_width
                print("Word is longer than max_width")
                return None

            lines[-1] = word
            curr_line_width = word_width
        else:
            #new_line_width = font.getlength(f"{lines[-1]}{word}")
            new_line_width, _ = base.getsize(f"{lines[-1]}{word}", font=font)

            if new_line_width > max_width:
                # Word is too long to fit on the current line
                #word_width = font.getlength(word)
                word_width, _ = base.getsize(word, font=font)
                new_num_lines = len(lines) + 1
                new_text_height = (new_num_lines * line_height) + (
                    new_num_lines * spacing
                )

                if word_width > max_width or new_text_height > max_height:
                    # Word is longer than max_width, and
                    # adding a new line would make the text too tall
                    print("Word is longer than max_width, adding a new line would make the text too tall")
                    return None

                if word.encode().isalpha() and lines[-1][-1].encode().isalpha():
                    lines[-1] = f"{lines[-1]}-"

                # Put the word on the next line
                lines.append(word)
                curr_line_width = word_width
            else:
                # Put the word on the current line
                lines[-1] = f"{lines[-1]}{word}"
                curr_line_width = new_line_width

    return "\n".join(lines)
