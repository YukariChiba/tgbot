from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import os

enabled = True


def load():
    print("RandomAnime Plugin Loaded!")


def isfloat(string):
    try:
        return float(string) and '.' in string
    except ValueError:
        return False


def checkarg(arg):
    if len(arg) == 0:
        return (random.randint(1000, 49999), 1.0)
    if len(arg) == 1 and arg[0].isnumeric():
        if int(arg[0]) > 999 and int(arg[0]) < 50000:
            return (int(arg[0]), 1.0)
    if len(arg) == 2 and arg[0].isnumeric() and isfloat(arg[1]):
        cr = round(float(arg[1]), 1)
        if int(arg[0]) > 999 and int(arg[0]) < 50000 and cr >= 0.3 and cr <= 2.0:
            return (int(arg[0]), cr)
    return (-1, -1)


def run(update: Update, context: CallbackContext) -> None:
    seedlist = checkarg(context.args)
    if seedlist[0] == -1:
        update.message.reply_text(
            "*Get a random anime from thisanimedoesnotexist.ai .*\nUsage: `/TADNE [seed] [creativity(0.3-2.0)]`.", parse_mode='Markdown')
    else:
        seed = str(seedlist[0])
        cr = str(seedlist[1])
        update.message.reply_photo(
            "https://thisanimedoesnotexist.ai/results/psi-{}/seed{}.png".format(cr, seed), caption="Random Seed: {}\nCreativity: {}".format(seed, cr), parse_mode='Markdown')


handlers = [CommandHandler("tadne", run)]
