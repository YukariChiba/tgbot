from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import base64
import os
from os import listdir
from os.path import isfile, join
import time
import shutil
import requests

enabled = True


def load():
    from utils.init import chk_dir
    chk_dir(os.getenv("CACHE_DIR") + "tmp/PassIn")
    print("UESTC Pass Plugin Loaded!")


def passin(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) == str(os.getenv("MODULE_PASS_ADMIN")):
        if len(context.args) == 0:
            context.bot.sendChatAction(
                chat_id=update.message.chat_id, action=ChatAction.TYPING)
            try:
                cred = os.getenv("MODULE_PASS_CREDENTIAL").split(":")
                cred_json = {
                    "password": cred[1],
                    "username": cred[0],
                    "verifyKey": ""
                }
                if (os.getenv("MODULE_PASS_MODE") == 'portal'):
                    req = requests.post(
                        'https://smaco2.uestc.edu.cn/shiroApi/auth/thirdpart/login?pipe=uestc-portal', json=cred_json)
                else:
                    req = requests.post(
                        'https://smaco2.uestc.edu.cn/shiroApi/auth', json=cred_json)
                reqjson = req.json()
                auth = reqjson["data"]["Authorization"]
                preq = requests.get(
                    'https://passport-api.nia.ac.cn/pipe/pass/getObjectQrcode', headers={'Authorization': auth})
                preq_json = preq.json()
                update.message.reply_photo(
                    "https://smaco2.uestc.edu.cn/qrcode" + preq_json["data"]["picPath"])
            except Exception as e:
                update.message.reply_text(
                    "`Server Error: {}`".format(type(e).__name__), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Get UESTC campus entrance code.*\nUsage: `/passin`.", parse_mode='Markdown')


handlers = [CommandHandler("passin", passin, run_async=True)]
