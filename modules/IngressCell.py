from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import requests
from PIL import Image
from utils.mapRender import getImageCluster
import os
import emoji

enabled = True

globe = ['AF', 'AS', 'NR', 'PA', 'AM', 'ST']

subarea = [
    'ALPHA', 'BRAVO', 'CHARLIE', 'DELTA',
    'ECHO', 'FOXTROT', 'GOLF', 'HOTEL',
    'JULIET', 'KILO', 'LIMA', 'MIKE',
    'NOVEMBER', 'PAPA', 'ROMEO', 'SIERRA',
]


def load():
    from utils.init import chk_dir
    chk_dir(os.getenv("CACHE_DIR") + "tmp/IngressCell")
    print("IngressCell Plugin Loaded!")


def checkarg(args):
    argarr = args[0].split("-")
    if len(argarr) != 3:
        return False
    if len(argarr[0]) != 4 or not argarr[0].isalnum():
        return False
    if argarr[1].upper() not in subarea or not argarr[1].isalpha():
        return False
    if len(argarr[2]) != 2 or not argarr[2].isnumeric():
        return False
    return True


def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text(emoji.emojize(
            ":globe_with_meridians: *Check the location of a Ingress cell.*\nUsage: `/cell {Cell ID}`."), parse_mode='Markdown')
    else:
        if not checkarg(context.args):
            update.message.reply_text(
                "`Invalid argument.`", parse_mode='Markdown')
        else:
            r = requests.get(
                'https://ingress-cells.appspot.com/query?cell=' + context.args[0])
            j = r.json()
            if 'error' in j:
                update.message.reply_text(
                    "`Error: Cell not exist.`", parse_mode='Markdown')
            else:
                context.bot.sendChatAction(
                    chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
                returnText = "*Cell*: `{0}`\n*S2 ID*: `{1}`".format(
                    j["name"], j["s2"])
                p1 = [min(j["geom"]["nw"][0], j["geom"]["ne"][0], j["geom"]["sw"][0], j["geom"]["se"][0]), min(
                    j["geom"]["nw"][1], j["geom"]["ne"][1], j["geom"]["sw"][1], j["geom"]["se"][1])]
                p2 = [max(j["geom"]["nw"][0], j["geom"]["ne"][0], j["geom"]["sw"][0], j["geom"]["se"][0]), max(
                    j["geom"]["nw"][1], j["geom"]["ne"][1], j["geom"]["sw"][1], j["geom"]["se"][1])]
                if not os.path.isfile(os.getenv("CACHE_DIR") + "tmp/IngressCell/" + j["s2"] + ".png"):
                    imagecluster = getImageCluster(
                        p1[0], p1[1], p2[0], p2[1], 8)
                    imagecluster.save(
                        os.getenv("CACHE_DIR") + "tmp/IngressCell/" + j["s2"] + ".png")
                update.message.reply_photo(
                    open(str(os.getenv("CACHE_DIR") + "tmp/IngressCell/" + j["s2"] + ".png"), "rb"), caption=returnText, parse_mode='Markdown')


handlers = [CommandHandler("cell", run, run_async=True)]
