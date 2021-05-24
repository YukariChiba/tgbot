from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import requests
import os
import emoji
import json
import shutil
from cairosvg import svg2png

enabled = True


def load():
    print("Graph42 Plugin Loaded!")


def getImage(asn, asn2=None):
    if asn2:
        if (asn.isnumeric() or (asn[:2].upper() == "AS" and asn[2:].isnumeric())) and (asn2.isnumeric() or (asn2[:2].upper() == "AS" and asn2[2:].isnumeric())):
            try:
                u = "http://info-api.nia.dn42/path_lookup/{}/{}".format(
                    asn, asn2)
                r = requests.get(u, stream=True)
                if r.status_code != 200:
                    return None
                with open(os.getenv("MODULE_GRAPH42_TMPIMG") + ".svg", "wb") as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                return os.getenv("MODULE_GRAPH42_TMPIMG") + ".svg"
            except Exception as e:
                return None
        else:
            return None
    else:
        if asn.isnumeric() or (asn[:2].upper() == "AS" and asn[2:].isnumeric()):
            try:
                u = "http://info-api.nia.dn42/as_graph/{}".format(asn)
                r = requests.get(u, stream=True)
                if r.status_code != 200:
                    return None
                with open(os.getenv("MODULE_GRAPH42_TMPIMG") + ".svg", "wb") as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                return os.getenv("MODULE_GRAPH42_TMPIMG") + ".svg"
            except Exception as e:
                return None
        else:
            return None


def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 1:
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        im = getImage(context.args[0])
        if im:
            svg2png(open(im, 'rb').read(), write_to=open(
                os.getenv("MODULE_GRAPH42_TMPIMG") + ".png", 'wb'))
            with open(os.getenv("MODULE_GRAPH42_TMPIMG") + ".png", "rb") as f:
                update.message.reply_photo(f)
        else:
            update.message.reply_text("`Not found.`", parse_mode='Markdown')
    elif len(context.args) == 2:
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        im = getImage(context.args[0], context.args[1])
        if im:
            svg2png(open(im, 'rb').read(), write_to=open(
                os.getenv("MODULE_GRAPH42_TMPIMG") + ".png", 'wb'))
            with open(os.getenv("MODULE_GRAPH42_TMPIMG") + ".png", "rb") as f:
                update.message.reply_photo(f)
        else:
            update.message.reply_text("`Not found.`", parse_mode='Markdown')
    else:
        update.message.reply_text(
            "*Get dn42 path graph.*\nUsage: `/graph42 {ASN} [to ASN]`.", parse_mode="Markdown")


handlers = [CommandHandler("graph42", run, run_async=True)]

if __name__ == "__main__":
    getImage("AS4242421331")
