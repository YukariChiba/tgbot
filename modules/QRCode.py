from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
from pyzbar.pyzbar import decode
from PIL import Image
import os

enabled = True


def load():
    print("QRCode Plugin Loaded!")


def run(update: Update, context: CallbackContext) -> None:
    reply_message = update.message.reply_to_message
    if reply_message and len(context.args) == 0:
        if reply_message.photo or reply_message.sticker:
            with open(os.getenv("MODULE_QRCODE_TMP"), 'r+b') as f:
                if reply_message.photo:
                    reply_message.photo[0].get_file().download(out=f)
                if reply_message.sticker:
                    reply_message.sticker.get_file().download(out=f)
                result = decode(Image.open(f))
            resultlist = []
            for decd in result:
                resultlist.append("`{}`\n".format(decd.data.decode("utf-8")))
            if len(resultlist) > 0:
                update.message.reply_text(
                    "*Content*: \n{}".format("".join(resultlist)), parse_mode='Markdown')
            else:
                update.message.reply_text(
                    "`Error: No QRCode found.`", parse_mode='Markdown')
        else:
            update.message.reply_text(
                "`Error: No image found.`", parse_mode='Markdown')
    else:
        update.message.reply_text(
            "*Scan a qrcode in replied message.*\nUsage: `/qrcode`.", parse_mode='Markdown')


handlers = [CommandHandler("qrcode", run)]
