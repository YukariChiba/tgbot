from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
from mcipc.rcon.je import Client
import base64
import os
from os import listdir
from os.path import isfile, join
import time
enabled = True


def load():
    from utils.init import chk_dir
    chk_dir(os.getenv("MODULE_MCRCON_PRESET"))
    print("MCRCON Plugin Loaded!")


def args_check_num(args, numset):
    if len(args) in numset:
        return True
    else:
        return False


def tick(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_num(context.args, [0, 1]):
            try:
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    resp = client.debug("start")
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
                    t = 10
                    if len(context.args) == 1:
                        tt = int(context.args[0])
                        if tt > 3 and tt < 20:
                            t = tt
                    time.sleep(t)
                    resp = client.debug("stop")
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Execute a profile to query tps.*\nUsage: `/mctick [time]`.", parse_mode='Markdown')


def custom(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_num(context.args, [1]):
            try:
                with open(os.getenv("MODULE_MCRCON_PRESET") + context.args[0]) as pf:
                    cmd = pf.read()
                cmddata = cmd.split("\n", 1)
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    resp = client.run(
                        cmddata[0].strip(), cmddata[1].strip())
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Execute custom command preset.*\nUsage: `/mcc <CommandPreset>`.", parse_mode='Markdown')


def customlist(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_num(context.args, [0]):
            presetfiles = [f for f in listdir(os.getenv("MODULE_MCRCON_PRESET")) if isfile(
                join(os.getenv("MODULE_MCRCON_PRESET"), f))]
            update.message.reply_text(
                "*Preset list*:\n\n" + "\n".join(presetfiles), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*List custom command preset.*\nUsage: `/mcclist`.", parse_mode='Markdown')


def kick(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_num(context.args, [1, 2]):
            try:
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    if len(context.args) == 2:
                        resp = client.kick(
                            context.args[0], context.args[1])
                    else:
                        resp = client.kick(context.args[0])
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Kick specific player from MC server.*\nUsage: `/mckick <Player> [Reason]`.", parse_mode='Markdown')


def banip(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_num(context.args, [1, 2]):
            try:
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    if len(context.args) == 2:
                        resp = client.banip(
                            context.args[0], context.args[1])
                    else:
                        resp = client.banip(context.args[0])
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Ban specific IP from MC server.*\nUsage: `/mcbanip <IP> [Reason]`.", parse_mode='Markdown')


def ban(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_num(context.args, [1, 2]):
            try:
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    if len(context.args) == 2:
                        resp = client.ban(
                            context.args[0], context.args[1])
                    else:
                        resp = client.ban(context.args[0])
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Ban specific player from MC server.*\nUsage: `/mcban <Player> [Reason]`.", parse_mode='Markdown')


def pardon(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_num(context.args, [1]):
            try:
                with Client(os.getenv("MODULE_MCRCON_SERVER"), 25575, passwd=os.getenv("MODULE_MCRCON_PASS")) as client:
                    resp = client.pardon(context.args[0])
                    update.message.reply_text(
                        "`" + resp + "`", parse_mode='Markdown')
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Removes specific player from banlist of MC server.*\nUsage: `/pardon <Player>`.", parse_mode='Markdown')


def banlist(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_MCRCON_ADMIN")):
        if args_check_num(context.args, [0]):
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


handlers = [CommandHandler("mctick", tick, run_async=True),
            CommandHandler("mcban", ban, run_async=True),
            CommandHandler("mcc", custom, run_async=True),
            CommandHandler("mcclist", customlist, run_async=True),
            CommandHandler("mcbanip", banip, run_async=True),
            CommandHandler("mcpardon", pardon, run_async=True),
            CommandHandler("mckick", kick, run_async=True),
            CommandHandler("mcbanlist", banlist, run_async=True)]
