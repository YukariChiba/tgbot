from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
from PIL import Image
from utils.mapRender import getImageCluster
import maidenhead as mh
import os

enabled = True

step = [[1, 2, 8], [1/24, 2/24, 13], [1/240, 2/240, 16]]


def load():
    print("Maidenhead Plugin Loaded!")


def checkarg(arg):
    if len(arg) >= 4 and len(arg) <= 12 and not arg.isalnum():
        return False
    return True


def run(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text(
            "*Check the location of a maidenhead code.*\nUsage: `/maidenhead {CODE}`.", parse_mode='Markdown')
    else:
        if not checkarg(context.args[0]):
            update.message.reply_text(
                "`Error: Invalid argument.`", parse_mode='Markdown')
        else:
            try:
                loc = mh.to_location(context.args[0])
            except ValueError:
                update.message.reply_text(
                    "`Error: Invalid argument.`", parse_mode='Markdown')
                return
            zonestep = step[0]
            if len(context.args[0]) > 4:
                zonestep = step[1]
            if len(context.args[0]) > 6:
                zonestep = step[2]
            context.bot.sendChatAction(
                chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            returnText = "*Code*: `{0}`".format(
                context.args[0].upper())
            if not os.path.isfile(os.getenv("MODULE_MAIDENHEAD_TMP") + context.args[0].upper() + ".png"):
                imagecluster = getImageCluster(
                    loc[0], loc[1], loc[0] + zonestep[0] * 1.1, loc[1] + zonestep[1] * 1.1, zonestep[2])
                imagecluster.save(
                    os.getenv("MODULE_MAIDENHEAD_TMP") + context.args[0].upper() + ".png")
            update.message.reply_photo(
                open(str(os.getenv("MODULE_MAIDENHEAD_TMP") + context.args[0].upper() + ".png"), "rb"), caption=returnText, parse_mode='Markdown')


handlers = [CommandHandler("maidenhead", run)]
