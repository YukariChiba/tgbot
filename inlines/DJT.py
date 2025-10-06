import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import random
import json
from utils.init import getEnvSafe

enabled = True

contentList = []

def load():
    global contentList
    with open(getEnvSafe("MODULE_INLINE_DJT_JSON")) as f:
        contentList = json.load(f)
    print("DJT Inline Plugin Loaded!")

def filter(arg: str):
    return arg == ""

def getDJT():
    return contentList[random.randint(0, len(contentList))]["content"]

def run():
    djt = getDJT()
    return_val = InlineQueryResultArticle(
        id=str(uuid4()), title="毒鸡汤", input_message_content=InputTextMessageContent(message_text=djt, parse_mode='Markdown'), description=djt, thumbnail_url=os.getenv("BOTAVATAR"))
    return return_val
