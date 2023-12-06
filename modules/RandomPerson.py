from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import os

enabled = False # API Broken


def load():
    print("RandomPerson Plugin Loaded!")


def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 0:
        update.message.reply_text(
            "*Get a random person from thispersondoesnotexist.com .*\nUsage: `/person`.", parse_mode='Markdown')
    else:
        update.message.reply_photo(
            "https://thispersondoesnotexist.com/image?rnd={}".format(str(random.randint(0, 31415926))))


handlers = [CommandHandler("person", run, run_async=True)]
