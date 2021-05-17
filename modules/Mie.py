from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import ipaddress
import subprocess
import os

enabled = True


def load():
    print("Mie Plugin Loaded!")


def run(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("咩～")


handlers = [CommandHandler("mie", run, run_async=True)]
