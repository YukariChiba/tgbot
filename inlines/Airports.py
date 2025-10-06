import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import csv

from telegram._inline.inlinequery import InlineQuery

from utils.init import getEnvSafe

enabled = True

airports = []


def load():
    global airports
    with open(getEnvSafe("MODULE_INLINE_AIRPORTDATA"), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(reader)
        airports = [{h:x for (h,x) in zip(headers,row)} for row in reader]
    print("Airports Inline Plugin Loaded!")


def filter(arg: str):
    global airports
    if arg == "":
        return False
    elif not arg.isalnum() or not (len(arg) == 4 or len(arg) == 3):
        return False
    elif len(arg) == 4:
        return any(p["icao"] == arg.upper() for p in airports)
    else:
        return any(p["iata"] == arg.upper() for p in airports)


def queryICAO(code: str):
    global airports
    if len(code) == 4:
        queryResult = [p for p in airports if p["icao"] == code.upper()]
    else:
        queryResult = [p for p in airports if p["iata"] == code.upper()]
    if len(queryResult) == 0:
        return ""
    airport = queryResult[0]
    return {"string": "*{airport}*\n*IATA:* `{iata}`\n*ICAO:* `{icao}`\n*Region:* {region_name}\n*Country:* {country_code}".format(**airport), "desc": airport["airport"]}


def run(querybody: InlineQuery, _):
    ICAO = queryICAO(querybody.query)
    if ICAO == "":
        return None
    return_val = InlineQueryResultArticle(
        id=str(uuid4()), title="机场 ICAO 查询", input_message_content=InputTextMessageContent(message_text=ICAO["string"], parse_mode='Markdown'), description=(querybody.query+": " + ICAO["desc"]), thumbnail_url=os.getenv("MODULE_INLINE_AIRPORT_AVATAR"))
    return return_val
