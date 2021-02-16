from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import json
import os
import emoji

enabled = True

dresslist = {}

def load():
    global dresslist
    with open(os.getenv("MODULE_DRESS_DATA")) as f:
        raw = json.load(f)
        dresslist = raw["hashTable"]
    print("RandomDress Plugin Loaded!")


def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 0:
        update.message.reply_text(
            emoji.emojize(":dress: *Get a random dress photo from `komeiji-satori/Dress`.*\nUsage: `/dress`."), parse_mode='Markdown')
    else:
        dress = random.choice(list(dresslist))
        update.message.reply_photo("https://satori.mycard.moe" + dress, caption="`{}`".format(dress), parse_mode='Markdown')


handlers = [CommandHandler("dress", run)]
