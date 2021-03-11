from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import requests
import os
import emoji
import json
import shutil

enabled = True

def load():
    print("Smokeping Plugin Loaded!")

def getImage(node):
    try:
        u = "http://ping-cn.nia.dn42/smokeping/cache/DN42/Ping42_Node/DN42NODE_{}_last_10800.png".format(node)
        r = requests.get(u, stream=True)
        if r.status_code != 200:
            return None
        with open(os.getenv("MODULE_SMOKE_TMPIMG"), "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return os.getenv("MODULE_SMOKE_TMPIMG")
    except Exception as e:
        return None

def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text("*Get smokeping graph.*\nUsage: `/smokeping {node}`.\n_See Smokeping First!_",parse_mode="Markdown")
    else:
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        im = getImage(context.args[0])
        if im:
            with open(im, "rb") as f:
                update.message.reply_photo(f)
                #update.message.reply_photo(f, caption="Node: `{}`".format(context.args[0]), parse_mode='Markdown')
        else:
            update.message.reply_text("`Not found.`",parse_mode='Markdown')


handlers = [CommandHandler("smoke", run)]

if __name__ == "__main__":
        getImage("ALI1")
