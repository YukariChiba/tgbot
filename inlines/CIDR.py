import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import ipaddress

from telegram._inline.inlinequery import InlineQuery

enabled = True


def load():
    print("CIDR Inline Plugin Loaded!")

def filter(arg: str):
    try:
        ipaddress.ip_interface(arg)
        return True
    except ValueError:
        return False

def getCIDR(itf: str):
    cidr = ipaddress.ip_interface(itf).network
    return "*Query*：`{0}`\n*Prefix*：`{1}`\n*Netmask*：`{2}`".format(itf, cidr.with_prefixlen, cidr.netmask)


def run(querybody: InlineQuery, _):
    cidr = getCIDR(querybody.query)
    return_val = InlineQueryResultArticle(
        id=str(uuid4()), title="CIDR", input_message_content=InputTextMessageContent(message_text=cidr, parse_mode='Markdown'), description=querybody.query + " 的 CIDR 写法", thumbnail_url=os.getenv("BOTAVATAR"))
    return return_val
