from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import ipaddress
import subprocess
import os

enabled = True


def load():
    print("NoComment Plugin Loaded!")


def run(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "有一说一，这件事大家懂得都懂，不懂得，说了你也不明白，不如不说。你们也别来问我怎么了，利益牵扯太大，说了对你们也没什么好处，当不知道就行了，其余的我只能说这里面水很深，牵扯到很多大人物。详细资料你们自己找是很难找的，网上大部分已经删除干净了，所以我只能说懂得都懂，不懂得也没办法。")


handlers = [CommandHandler("dddd", run, run_async=True)]
