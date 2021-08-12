from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import random
import os
import json

enabled = True

prob_list = []


def load():
    global prob_list
    with open("data/Reborn/rate.json") as f:
        prob_list = json.load(f)
    print("Reborn Plugin Loaded!")


def random_country():
    global prob_list
    return random.choices(
        population=[i["name"] for i in prob_list],
        weights=[float(i["weight"]) for i in prob_list],
        k=1
    )[0]


def random_gender():
    return random.choices(
        population=["男孩子", "女孩子", "雌雄同体"],
        weights=[0.50707, 0.48292, 0.01001],
        k=1
    )[0]


def random_all():
    if random.random() > 0.1:
        return "投胎成功！\n您出生在 *{}*, 是 *{}*。".format(random_country(), random_gender())
    else:
        return "投胎失败！\n您没能活到出生，祝您下次好运！"


def checkarg(arg):
    if len(arg) == 0:
        return random.randint(0, 100000)
    if len(arg) == 1:
        if len(arg[0]) <= 20:
            return int(arg[0])
    return -1


def run(update: Update, context: CallbackContext) -> None:
    seed = checkarg(context.args)
    if seed == -1:
        update.message.reply_text(
            "*Give you a chance to reborn.*\nUsage: `/reborn [seed]`.", parse_mode='Markdown')
    else:
        update.message.reply_text(random_all(), parse_mode='Markdown')


handlers = [CommandHandler("reborn", run, run_async=True)]


def test():
    load()
    print(random_all())


if __name__ == "__main__":
    test()
