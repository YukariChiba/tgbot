from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import json
import os
import emoji
import re

enabled = True

dresslist = {}
dresslist_images = []


def load():
    global dresslist
    global dresslist_raw
    global dresslist_images_weight
    with open(os.getenv("MODULE_DRESS_DATA")) as f:
        raw = json.load(f)
        dresslist_raw = raw["hashTable"]
    dresslist_raw = list(dresslist_raw)
    for dress_item in dresslist_raw:
        if dress_item.startswith("/Dress/"):
            dresslist_images.append(dress_item)
            tmp = dress_item.split("/")
            if len(tmp) >= 3:
                dresslist.setdefault(tmp[2], []).append(dress_item)
    if not os.path.exists(os.getenv("MODULE_DRESS_VOTE_DATA")):
        with open(os.getenv("MODULE_DRESS_VOTE_DATA"), "w") as f:
            json.dump({}, f)
    print("RandomDress Plugin Loaded!")


def makeReplyMarkup(dress):
    keyboard = [
        [
            InlineKeyboardButton("好耶", callback_data='/dress upvote ' + dress),
            InlineKeyboardButton(
                "坏耶", callback_data='/dress downvote ' + dress)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def voteCallback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    info = query.data.split(" ")
    if len(info) != 3:
        return
    if info[2] not in dresslist_images:
        return
    with open(os.getenv("MODULE_DRESS_VOTE_DATA")) as f:
        raw = json.load(f)
    if info[2] not in raw:
        raw[info[2]] = {"upvote": [], "downvote": []}
    if info[1] not in raw[info[2]]:
        raw[info[2]][info[1]] = []
    if query.from_user.id not in raw[info[2]][info[1]]:
        raw[info[2]][info[1]].append(query.from_user.id)
    with open(os.getenv("MODULE_DRESS_VOTE_DATA"), "w") as f:
        json.dump(raw, f)
    #query.edit_message_reply_markup(reply_markup=None)
    query.answer(text="感谢您的评价。")


def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) >= 1:
        if len(context.args) == 1 and re.match(r"[a-zA-Z0-9\-]", context.args[0]):
            if context.args[0] in dresslist.keys():
                dress = random.choice(dresslist[context.args[0]])
                update.message.reply_photo(
                    "https://satori.mycard.moe" + dress, caption="`{}`".format(dress), parse_mode='Markdown', reply_markup=makeReplyMarkup(dress))
            else:
                update.message.reply_text(
                    "`Error: Not found.`", parse_mode='Markdown')
        else:
            update.message.reply_text(
                emoji.emojize(":dress: *Get a random dress photo from* `komeiji-satori/Dress`.\nUsage: `/dress [User ID]`."), parse_mode='Markdown')
    else:
        user = random.choice(list(dresslist.keys()))
        dress = random.choice(dresslist[user])
        update.message.reply_photo(
            "https://satori.mycard.moe" + dress, caption="`{}`".format(dress), parse_mode='Markdown', reply_markup=makeReplyMarkup(dress))


handlers = [CommandHandler("dress", run, run_async=True),
            CallbackQueryHandler(voteCallback, pattern=r'\/dress (upvote|downvote) (\S)+', run_async=True)]
