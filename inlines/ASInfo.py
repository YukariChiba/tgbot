import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import requests
from telegram._inline.inlinequery import InlineQuery

from utils.init import getEnvSafe

enabled = True


def load():
    print("ASInfo Inline Plugin Loaded!")


def filter(arg: str):
    if arg == "" or len(arg) < 5 or len(arg) > 12:
        return False
    else:
        return arg[2:].isnumeric() and (arg.startswith("AS") or arg.startswith("as"))


def resultText(obj, key):
    if key in obj:
        return obj[key][0]
    else:
        return "Null"


def processResult(res):
    with open(getEnvSafe("MODULE_INLINE_ASINFO_TPL"), 'r') as file:
        tpl = file.read()
    asn = res["asn"]
    routes = res["routes"]
    return tpl.format(resultText(asn, "aut-num"), resultText(asn, "as-name"), resultText(asn, "mnt-by"), resultText(asn["contact-info"], "person"), resultText(asn["contact-info"], "contact"), "\n".join([x["route"][0] for x in routes["ipv4"]]), "\n".join([x["route6"][0] for x in routes["ipv6"]]))


def getASN(asn):
    return_value = ""
    r = requests.get(
        'https://bgp-data.strexp.net/asn/AS' + asn + '.json')
    if r.status_code == 404:
        return None
    return r.json()


def run(querybody: InlineQuery, context):
    asn_info = getASN(querybody.query[2:])
    if asn_info == None:
        return None
    return_val = InlineQueryResultArticle(
        id=str(uuid4()), title="DN42 ASN", input_message_content=InputTextMessageContent(message_text=processResult(asn_info), parse_mode='Markdown'), description=(querybody.query+" in DN42"), thumbnail_url=os.getenv("BOTAVATAR"))
    return return_val
