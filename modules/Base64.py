from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import base64
import os

enabled = True


def load():
    print("Base64 Plugin Loaded!")

def _help_de(update: Update):
    update.message.reply_text(
            "*Base64 decode.*\nUsage: `/b64de [code]`.", parse_mode='Markdown')

def _help_en(update: Update):
    update.message.reply_text(
            "*Base64 encode.*\nUsage: `/b64en <text>`.", parse_mode='Markdown')

def run_de(update: Update, context: CallbackContext) -> None:
    reply_message = update.message.reply_to_message
    if len(context.args) == 1:
        if len(context.args[0]) < 120:
            try:
                update.message.reply_text("Base64 decode result:\n`{}`".format(base64.b64decode(context.args[0]).decode()), parse_mode='Markdown')
            except:
                update.message.reply_text(
                    "`Error: Invalid code.`", parse_mode='Markdown')
        else:
            update.message.reply_text(
                    "`Error: Code too long.`", parse_mode='Markdown')
    elif reply_message and len(context.args) == 0:
        if len(reply_message.text) < 50:
            try:
                update.message.reply_text("Base64 decode result:\n`{}`".format(base64.b64decode(reply_message.text).decode()), parse_mode='Markdown')
            except:
                update.message.reply_text(
                    "`Error: Invalid code.`", parse_mode='Markdown')
        else:
            update.message.reply_text(
                    "`Error: Code too long or invalid.`", parse_mode='Markdown')
    else:
        _help_de(update)

def run_en(update: Update, context: CallbackContext) -> None:
    reply_message = update.message.reply_to_message
    if len(context.args) >= 1:
        txt = " ".join(context.args)
        if len(txt) < 50:
            update.message.reply_text("Base64 encode result:\n`{}`".format(base64.b64encode(str.encode(txt)).decode()), parse_mode='Markdown')
        else:
            update.message.reply_text(
                    "`Error: Message too long.`", parse_mode='Markdown')
    elif reply_message and len(context.args) == 0:
        if len(reply_message.text) < 50:
            update.message.reply_text("Base64 encode result:\n`{}`".format(base64.b64encode(str.encode(reply_message.text)).decode()), parse_mode='Markdown')
        else:
            update.message.reply_text(
                    "`Error: Message too long or invalid.`", parse_mode='Markdown')
    else:
        _help_en(update)


handlers = [CommandHandler("b64en", run_en, run_async=True), CommandHandler("b64de", run_de, run_async=True)]
