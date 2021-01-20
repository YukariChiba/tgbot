from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import os

enabled = True


def load():
    print("RandomCat Plugin Loaded!")

def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 0:
        update.message.reply_text(
            "*Get a random cat from thiscatdoesnotexist.com .*\nUsage: `/cat`.", parse_mode='Markdown')
    else:
        update.message.reply_photo(
            "https://thiscatdoesnotexist.com")


handlers = [CommandHandler("cat", run)]
