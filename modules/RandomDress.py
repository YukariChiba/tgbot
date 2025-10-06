from telegram.ext import ContextTypes, CommandHandler
from telegram import Update
from utils.init import getEnvSafe
import random
import json
import os
import emoji
import re

enabled = True

dresslist = {}
dresslist_images = []

dresslist_lite = {}
dresslist_lite_images = []

dressupstream = "https://github.com/Cute-Dress/Dress/blob/master"
dressupstream_lite = "https://github.com/KiritakeKumi/Dress-Lite/blob/master"

def formatMsg(photo):
    msg = "Location: `{}`".format(photo)
    return msg


def load():
    global dresslist
    global dresslist_images
    global dresslist_lite
    global dresslist_lite_images
    with open(getEnvSafe("MODULE_DRESS_DATA")) as f:
        dresslist = json.load(f)
    with open(getEnvSafe("MODULE_DRESS_LITE_DATA")) as f:
        dresslist_lite = json.load(f)
    for username in dresslist.keys():
        dresslist_images = dresslist_images + dresslist[username]
    for username in dresslist_lite.keys():
        dresslist_lite_images = dresslist_lite_images + dresslist[username]
    if not os.path.exists(getEnvSafe("MODULE_DRESS_VOTE_DATA")):
        with open(getEnvSafe("MODULE_DRESS_VOTE_DATA"), "w") as f:
            json.dump({}, f)
    print("RandomDress Plugin Loaded!")


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args and len(context.args) >= 1:
        if len(context.args) == 1 and re.match(r"@?[a-zA-Z0-9\-]", context.args[0]):
            if context.args[0][0] == "@":
                context.args[0] = context.args[0][1:]
            if context.args[0] in dresslist.keys():
                dress = random.choice(dresslist[context.args[0]])
                await update.message.reply_photo(
                    dressupstream + dress + "?raw=true", caption=formatMsg(dress), parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "`Error: Not found.`", parse_mode='Markdown')
        else:
            await update.message.reply_text(
                emoji.emojize(":dress: *Get a random dress photo from* `komeiji-satori/Dress`.\nUsage: `/dress [User ID]`."), parse_mode='Markdown')
    else:
        user = random.choice(list(dresslist.keys()))
        dress = random.choice(dresslist[user])
        await update.message.reply_photo(
            dressupstream + dress + "?raw=true", caption=formatMsg(dress), parse_mode='Markdown')


async def runlite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args and len(context.args) >= 1:
        if len(context.args) == 1 and re.match(r"@?[a-zA-Z0-9\-]", context.args[0]):
            if context.args[0][0] == "@":
                context.args[0] = context.args[0][1:]
            if context.args[0] in dresslist_lite.keys():
                dress = random.choice(dresslist[context.args[0]])
                await update.message.reply_photo(
                    dressupstream_lite + dress + "?raw=true", caption=formatMsg(dress), parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "`Error: Not found.`", parse_mode='Markdown')
        else:
            await update.message.reply_text(
                emoji.emojize(":dress: *Get a random dress photo from* `KiritakeKumi/Dress-Lite`.\nUsage: `/dresslite [User ID]`."), parse_mode='Markdown')
    else:
        user = random.choice(list(dresslist_lite.keys()))
        dress = random.choice(dresslist_lite[user])
        await update.message.reply_photo(
            dressupstream_lite + dress + "?raw=true", caption=formatMsg(dress), parse_mode='Markdown')


handlers = [CommandHandler("dress", run, block=False),
            CommandHandler("dresslite", runlite, block=False)]


def test():
    from dotenv import load_dotenv
    load_dotenv()
    load()
    print(random.choice(dresslist[random.choice(list(dresslist.keys()))]))


if __name__ == "__main__":
    test()
