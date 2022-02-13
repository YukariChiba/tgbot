from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
from mcipc.rcon.je import Client
import base64
import os
enabled = True


def load():
    print("MCRCON Plugin Loaded!")


def args_check_banlist(args):
    if len(args) == 0:
        return True
    else:
        return False


def args_check_ban(args):
    if len(args) == 1:
        return True
    else:
        return False


def kick(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_ban(context.args):
            try:
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    resp = client.kick(context.args[0])
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Kick specific player from MC server.*\nUsage: `/mckick <Player>`.", parse_mode='Markdown')


def ban(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_ban(context.args):
            try:
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    resp = client.ban(context.args[0])
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Ban specific player from MC server.*\nUsage: `/mcban <Player>`.", parse_mode='Markdown')


def banlist(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_banlist(context.args):
            try:
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    resp = client.banlist().replace(".", "\n").replace(" bans:", " bans:\n")
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Get the banlist of MC server.*\nUsage: `/mcbanlist`.", parse_mode='Markdown')


handlers = [CommandHandler("mcban", ban, run_async=True),
            CommandHandler("mckick", kick, run_async=True),
            CommandHandler("mcbanlist", banlist, run_async=True)]
