from pathlib import Path
import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import random
import requests

enabled = True


def load():
    print("Couplet Inline Plugin Loaded!")


def filter(arg):
    return _ifAllChinese(arg)


def _ifAllChinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            if _char != '，' and _char != "？" and _char != "。" and _char != "？":
                return False
    return True


def getCouplet(querybody):
    try:
        r = requests.get(
            'https://ai-backend.binwang.me/chat/couplet/{}'.format(querybody))
        j = r.json()
        if j:
            return {"text": "*上联*: \n{}\n\n*下联*: \n{}".format(querybody, j["output"]), "preview": "下联： " + j["output"]}
        else:
            return None
    except:
        return None


def run(querybody, context):
    couplet = getCouplet(querybody.query)
    if couplet:
        return_val = InlineQueryResultArticle(
            id=uuid4(), title="对联", input_message_content=InputTextMessageContent(message_text=couplet["text"], parse_mode='Markdown'), description=couplet["preview"], thumb_url=os.getenv("MODULE_INLINE_COUPLET_AVATAR", "https://i.loli.net/2021/08/17/BRdNcP1rw72m9kz.jpg"))
        return return_val
    else:
        return None
