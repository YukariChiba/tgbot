from pathlib import Path
import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import dice

enabled = True

NOCACHE = True

def load():
    print("Dice Inline Plugin Loaded!")


def filter(arg):
    try:
        d = dice.roll(arg)
        return d.random_element.amount < 20 and d.random_element.sides < 1000000
    except Exception as e:
        return False

def getDice(dice_text):
    elements = list(dice.roll(dice_text))
    elements.sort()
    return "*投掷了骰子 [{}]*\n结果为:\n{}\n总和为: {}".format(dice_text, str(elements), sum(elements))

def run(querybody, context):
    result = getDice(querybody.query)
    return_val = InlineQueryResultArticle(
        id=uuid4(), title="骰子: " + querybody.query, input_message_content=InputTextMessageContent(message_text=result, parse_mode='Markdown'), description="掷出一枚骰子。", thumb_url=os.getenv("MODULE_INLINE_DICE_AVATAR"))
    return return_val
