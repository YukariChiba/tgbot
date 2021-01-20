from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import os

enabled = True


def load():
    print("RandomWaifu Plugin Loaded!")


def checkarg(arg):
    if len(arg) == 0:
        return random.randint(0, 100000)
    if len(arg) == 1 and arg[0].isnumeric():
        if int(arg[0]) >= 0 and int(arg[0]) <= 100000:
            return int(arg[0])
    return -1


def run(update: Update, context: CallbackContext) -> None:
    seed = checkarg(context.args)
    if seed == -1:
        update.message.reply_text(
            "*Get a random waifu from thiswaifudoesnotexist.net .*\nUsage: `/TWDNE [seed]`.", parse_mode='Markdown')
    else:
        seed = str(seed)
        update.message.reply_photo(
            "https://www.thiswaifudoesnotexist.net/example-{}.jpg".format(seed), caption="Random Seed: {}".format(seed), parse_mode='Markdown')


handlers = [CommandHandler("twdne", run), CommandHandler("waifu", run)]
