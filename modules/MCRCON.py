from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
from mcipc.rcon.je import Client
import base64
import os
enabled = True


def load():
    print("MCRCON Plugin Loaded!")


def args_check_ban(args):
    if len(args) == 1:
        return True
    else:
        return False


def ban(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_ban(context.args):
            try:
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    resp = client.ban(context.args[0])
                    update.message.reply_text(
                            "`+" + resp + "+`", parse_mode='Markdown')
            except:
                update.message.reply_text(
                        "`Server Error.`", parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Ban specific player from MC server.*\nUsage: `/mcban <Player>`.", parse_mode='Markdown')


handlers = [CommandHandler("mcban", ban, run_async=True)]
