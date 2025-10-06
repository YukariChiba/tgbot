from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
from telegram.constants import ChatAction
from utils.init import getEnvSafe
from utils.mapRender import getImageCluster
import maidenhead as mh
import os
import emoji

enabled = True

step = [[1, 2, 8], [1/24, 2/24, 13], [1/240, 2/240, 16]]


def load():
    from utils.init import chk_dir
    chk_dir(getEnvSafe("CACHE_DIR") + "tmp/Maidenhead")
    print("Maidenhead Plugin Loaded!")


def checkarg(arg: str):
    if len(arg) >= 4 and len(arg) <= 12 and not arg.isalnum():
        return False
    return True


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(emoji.emojize(
            ":globe_with_meridians: *Check the location of a maidenhead code.*\nUsage: `/maidenhead {CODE}`."), parse_mode='Markdown')
    else:
        if not checkarg(context.args[0]):
            await update.message.reply_text(
                "`Error: Invalid argument.`", parse_mode='Markdown')
        else:
            try:
                loc = mh.to_location(context.args[0])
            except ValueError:
                await update.message.reply_text(
                    "`Error: Invalid argument.`", parse_mode='Markdown')
                return
            zonestep = step[0]
            if len(context.args[0]) > 4:
                zonestep = step[1]
            if len(context.args[0]) > 6:
                zonestep = step[2]
            await context.bot.sendChatAction(
                chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            returnText = "*Code*: `{0}`".format(
                context.args[0].upper())
            if not os.path.isfile(getEnvSafe("CACHE_DIR") + "tmp/Maidenhead/" + context.args[0].upper() + ".png"):
                imagecluster = getImageCluster(
                    loc[0], loc[1], loc[0] + zonestep[0] * 1.1, loc[1] + zonestep[1] * 1.1, zonestep[2])
                imagecluster.save(
                    getEnvSafe("CACHE_DIR") + "tmp/Maidenhead/" + context.args[0].upper() + ".png")
            await update.message.reply_photo(
                open(str(getEnvSafe("CACHE_DIR") + "tmp/Maidenhead/" + context.args[0].upper() + ".png"), "rb"), caption=returnText, parse_mode='Markdown')


handlers = [CommandHandler("maidenhead", run, block=False)]
