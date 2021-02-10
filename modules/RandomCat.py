from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import os
import emoji

enabled = True


def load():
    print("RandomCat Plugin Loaded!")


def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 0:
        update.message.reply_text(
            emoji.emojize(":cat_face: *Get a random cat from thiscatdoesnotexist.com .*\nUsage: `/cat`."), parse_mode='Markdown')
    else:
        update.message.reply_photo(
            "https://thiscatdoesnotexist.com/?rnd={}".format(str(random.randint(0, 31415926))))


handlers = [CommandHandler("cat", run)]
