from telegram.ext import ContextTypes, CommandHandler
from telegram import Update
from telegram.constants import ChatAction
from pyzbar.pyzbar import decode
from PIL import Image
import os

from utils.init import getEnvSafe

enabled = True


def load():
    from utils.init import chk_dir
    chk_dir(getEnvSafe("CACHE_DIR") + "tmp/QRCode")
    print("QRCode Plugin Loaded!")


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = update.message.reply_to_message
    if reply_message and len(context.args or []) == 0:
        if reply_message.photo or reply_message.sticker:
            with open(getEnvSafe("CACHE_DIR") + "tmp/QRCode/qrcode.png" , 'w+b') as f:
                if reply_message.photo:
                    reply_message.photo[0].get_file().download(out=f)
                if reply_message.sticker:
                    reply_message.sticker.get_file().download(out=f)
                result = decode(Image.open(f))
            resultlist = []
            for decd in result:
                resultlist.append("`{}`\n".format(decd.data.decode("utf-8")))
            if len(resultlist) > 0:
                await update.message.reply_text(
                    "*Content*: \n{}".format("".join(resultlist)), parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "`Error: No QRCode found.`", parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "`Error: No image found.`", parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "*Scan a qrcode in replied message.*\nUsage: `/qrcode`.", parse_mode='Markdown')


handlers = [CommandHandler("qrcode", run, block=False)]
