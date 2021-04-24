from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import requests
import os
import emoji
import json

enabled = False

netmap = {}

def load():
    global netmap
    with open(os.getenv("MODULE_NETSTATUS_IFLIST")) as f:
        netmap = json.load(f)
    print("Net Status Plugin Loaded!")

def getNetStatus():
    global netmap
    try:
        r = requests.get("http://status-cn.nia.dn42/json.php")
        j = r.json()
        t = "*NIACN Network Status*:\n"
        for itf in j:
            ifname = itf
            if itf in netmap.keys():
                ifname = netmap[itf]
            status = ":question:"
            if j[itf]["status"] == "up":
                status = ":check_mark:"
            if j[itf]["status"] == "down":
                status = ":cross_mark:"
            t = t + "`{0}`: {1}\n".format(ifname, status)
        return t
    except:
        return None

def run(update: Update, context: CallbackContext) -> None:
    ns = getNetStatus()
    if ns:
        update.message.reply_text(emoji.emojize(ns),parse_mode='Markdown')
    else:
        update.message.reply_text("`Network Error.`",parse_mode='Markdown')


handlers = [CommandHandler("netstatus", run)]
