from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import os
import json

enabled = True

randint = 0

def load():
    print("FortuneTelling Plugin Loaded!")

def run(update: Update, context: CallbackContext) -> None:
    page = random.randint(1, 100)
    if len(context.args) != 0:
        update.message.reply_text(
            "*Get a senso ji omikuji*\nUsage: `/senso`.", parse_mode='Markdown')
    else:
        update.message.reply_media_group(["https://raw.githubusercontent.com/fumiama/senso-ji-omikuji/main/{}_0.jpg".format(str(page)),
        "https://raw.githubusercontent.com/fumiama/senso-ji-omikuji/main/{}_1.jpg".format(str(page))])


handlers = [CommandHandler("senso", run, run_async=True)]
