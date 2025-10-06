from pathlib import Path
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import requests
from telegram._inline.inlinequery import InlineQuery

from utils.init import getEnvSafe

enabled = True

def load():
    print("HHSH Inline Plugin Loaded!")

def filter(arg: str):
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

def getWords(hhsh: str):
    return_value = ""
    r = requests.post(
        'https://lab.magiconch.com/api/nbnhhsh/guess', data={"text": hhsh})
    j = r.json()
    if j == []:
        return ""
    for searchWord in j:
        return_value = return_value + processResult(searchWord)
    return return_value

def run(querybody: InlineQuery, _):
    hhsh = getWords(querybody.query)
    if hhsh == "":
        return None
    return_val = InlineQueryResultArticle(
        id=str(uuid4()), title="好好说话", input_message_content=InputTextMessageContent(message_text=hhsh, parse_mode='Markdown'), description=(querybody.query+"的意思"), thumbnail_url=getEnvSafe("BOTAVATAR"))
    return return_val
