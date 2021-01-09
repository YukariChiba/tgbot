from pathlib import Path
import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import random
import requests

enabled = True

def load():
    print("HHSH Inline Plugin Loaded!")

def filter(arg):
    if arg == "":
        return False
    else:
        words = arg.split()
        if len(words) != 1:
            return False
        else:
            word = words[0]
            return word.isalnum()

def processResult(res):
    if "trans" in res.keys():
        if res["trans"] == []:
            return ""
        hhshList = ', '.join(res["trans"])
    elif "inputting" in res.keys():
        if res["inputting"] == []:
            return ""
        hhshList = ', '.join(res["inputting"])
    else:
        return ""
    return '*' + res["name"] + ' 的意思：*\n' + hhshList + "\n"

def getWords(hhsh):
    return_value = ""
    r = requests.post(
        'https://lab.magiconch.com/api/nbnhhsh/guess', data={"text": hhsh})
    j = r.json()
    if j == []:
        return ""
    for searchWord in j:
        return_value = return_value + processResult(searchWord)
    return return_value

def run(querybody, context):
    hhsh = getWords(querybody.query)
    if hhsh == "":
        return None
    return_val = InlineQueryResultArticle(
        id=uuid4(), title="好好说话", input_message_content=InputTextMessageContent(message_text=hhsh, parse_mode='Markdown'), description=(querybody.query+"的意思"), thumb_url=os.getenv("BOTAVATAR"))
    return return_val
