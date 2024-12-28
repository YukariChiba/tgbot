from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.utils.helpers import escape_markdown
import random
import os
import json

enabled = True

def load():
    print("FortuneTelling Plugin Loaded!")

def run_senso(update: Update, context: CallbackContext) -> None:
    page = random.randint(1, 100)
    page_1 = InputMediaPhoto("https://raw.githubusercontent.com/fumiama/senso-ji-omikuji/main/{}_0.jpg".format(str(page)))
    page_2 = InputMediaPhoto("https://raw.githubusercontent.com/fumiama/senso-ji-omikuji/main/{}_1.jpg".format(str(page)))
    if len(context.args) != 0:
        update.message.reply_text(
            "*Get a senso ji omikuji*\nUsage: `/senso`.", parse_mode='Markdown')
    else:
        update.message.reply_media_group([page_1, page_2])

def run_keifuk(update: Update, context: CallbackContext) -> None:
    page = random.randint(1, 100)
    page_1 = "https://taonet.siksikyuen.org.hk/images/StickEnquiry/stickPaper/{}.png".format(str(page))
    if len(context.args) != 0:
        update.message.reply_text(
            "*Get a siksikyuen keifuk*\nUsage: `/siksikyuen`.", parse_mode='Markdown')
    else:
        update.message.reply_photo(page_1, caption="https://taonet.siksikyuen.org.hk/StickEnquiry/{}/zh-TW".format(str(page)), parse_mode="Markdown")

handlers = [
    CommandHandler("senso", run_senso, run_async=True),
    CommandHandler("keifuk", run_keifuk, run_async=True)
]
