from pathlib import Path
import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import random
import requests
import csv

enabled = True

airports = []


def load():
    global airports
    with open(os.getenv("MODULE_INLINE_AIRPORTDATA"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            airports.append(row)
    print("Airports Inline Plugin Loaded!")


def filter(arg):
    global airports
    if arg == "":
        return False
    elif not arg.isalnum() or not (len(arg) == 4 or len(arg) == 3):
        return False
    elif len(arg) == 4:
        return any(p[5] == arg.upper() for p in airports)
    else:
        return any(p[4] == arg.upper() for p in airports)


def queryICAO(code):
    global airports
    if len(code) == 4:
        queryResult = [p for p in airports if p[5] == code.upper()]
    else:
        queryResult = [p for p in airports if p[4] == code.upper()]
    if len(queryResult) == 0:
        return ""
    airport = queryResult[0]
    return {"string": "*{0}*\n*IATA:* `{1}`\n*ICAO:* `{2}`\n*City:* {3}\n*Country:* {4}".format(airport[1], airport[4], airport[5], airport[2], airport[3]), "desc": airport[1]}


def run(querybody, context):
    ICAO = queryICAO(querybody.query)
    if ICAO == "":
        return None
    return_val = InlineQueryResultArticle(
        id=uuid4(), title="机场 ICAO 查询", input_message_content=InputTextMessageContent(message_text=ICAO["string"], parse_mode='Markdown'), description=(querybody.query+": " + ICAO["desc"]), thumb_url=os.getenv("MODULE_INLINE_AIRPORT_AVATAR"))
    return return_val
