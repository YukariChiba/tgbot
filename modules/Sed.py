from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import re
import subprocess
import os

enabled = True


def load():
    print("Sed Plugin Loaded!")


def run(update: Update, context: CallbackContext) -> None:
    reply_message = update.message.reply_to_message
    if reply_message and len(context.args) == 2:
        if reply_message.text:
            if len(context.args[0]) < 18 and len(context.args[1]) < 18:
                replaced_text = re.sub(
                    context.args[0], context.args[1], reply_message.text)
                if len(replaced_text) < 500:
                    update.message.reply_text("Replace `{0}` with `{1}`: \n\n{2}".format(
                        context.args[0], context.args[1], replaced_text), parse_mode='Markdown')
                else:
                    update.message.reply_text(
                        "`Error: Result too long.`", parse_mode='Markdown')
            else:
                update.message.reply_text(
                    "`Error: Keyword too long.`", parse_mode='Markdown')
        else:
            update.message.reply_text(
                "`Error: No text found.`", parse_mode='Markdown')
    else:
        update.message.reply_text(
            "*Sed to the replied message.*\nUsage: `/sed {from_regex} {to_regex}`.", parse_mode='Markdown')


handlers = [CommandHandler("sed", run, run_async=True)]
