from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import json
import os
import emoji
import re

enabled = True

dresslist = []

def load():
    global dresslist
    with open(os.getenv("MODULE_DRESS_DATA")) as f:
        raw = json.load(f)
        dresslist_raw = raw["hashTable"]
    dresslist_raw = list(dresslist_raw)
    for dress_item in dresslist_raw:
        if dress_item.startswith("/Dress/"):
            dresslist.append(dress_item)
    print("RandomDress Plugin Loaded!")


def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) >= 1:
        if len(context.args) == 1 and context.args[0].isalnum():
            userlist = [i for i in dresslist if "/Dress/{}/".format(context.args[0]) in i]
            if len(userlist):
                dress = random.choice(userlist)
                update.message.reply_photo("https://satori.mycard.moe" + dress, caption="`{}`".format(dress), parse_mode='Markdown')
            else:
                update.message.reply_text("`Error: Not found.`", parse_mode='Markdown')
        else:
            update.message.reply_text(
                emoji.emojize(":dress: *Get a random dress photo from* `komeiji-satori/Dress`.\nUsage: `/dress [User ID]`."), parse_mode='Markdown')
    else:
        dress = random.choice(dresslist)
        update.message.reply_photo("https://satori.mycard.moe" + dress, caption="`{}`".format(dress), parse_mode='Markdown')


handlers = [CommandHandler("dress", run)]
