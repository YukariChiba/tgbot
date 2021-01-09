from pathlib import Path
import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import random
import requests
import csv

enabled = True


def load():
    print("YesOrNot Inline Plugin Loaded!")


def filter(arg):
    if arg == "":
        return False
    elif arg.endswith("?") or arg.endswith("？"):
        return True
    else:
        return False


def run(querybody, context):
    randVal = random.randint(1, 100)
    if randVal%2 == 1:
        randVal = "准 / Yes"
    else:
        randVal = "不准 / No"
    retStr = '*问题：' + querybody.query + '*\n回答：' + randVal
    return_val = InlineQueryResultArticle(
        id=uuid4(), title="准 (Yes) 还是 不准 (No)？", input_message_content=InputTextMessageContent(message_text=retStr, parse_mode='Markdown'), description=(querybody.query+" 的解答"), thumb_url=os.getenv("BOTAVATAR"))
    return return_val
