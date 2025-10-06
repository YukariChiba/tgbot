import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import requests

enabled = True


def load():
    print("YiYan Inline Plugin Loaded!")

def filter(arg: str):
    return arg == ""

def getYiYan():
    r = requests.get('https://v1.hitokoto.cn')
    j = r.json()
    return {"md": j["hitokoto"] + "\n\t_--" + j["from"] + "_", "desc": j["hitokoto"]}


def run():
    yiyan = getYiYan()
    return_val = InlineQueryResultArticle(
        id=str(uuid4()), title="一言", input_message_content=InputTextMessageContent(message_text=yiyan["md"], parse_mode='Markdown'), description=yiyan["desc"], thumbnail_url=os.getenv("BOTAVATAR"))
    return return_val
