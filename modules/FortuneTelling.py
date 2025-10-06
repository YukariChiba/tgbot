from telegram.ext import ContextTypes, CommandHandler
from telegram import Update, InputMediaPhoto
import random

enabled = True

def load():
    print("FortuneTelling Plugin Loaded!")

async def run_senso(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    page = random.randint(1, 100)
    page_1 = InputMediaPhoto("https://raw.githubusercontent.com/fumiama/senso-ji-omikuji/main/{}_0.jpg".format(str(page)))
    page_2 = InputMediaPhoto("https://raw.githubusercontent.com/fumiama/senso-ji-omikuji/main/{}_1.jpg".format(str(page)))
    if context.args and len(context.args) != 0:
        await update.message.reply_text(
            "*Get a senso ji omikuji*\nUsage: `/senso`.", parse_mode='Markdown')
    else:
        await update.message.reply_media_group([page_1, page_2])

async def run_keifuk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    page = random.randint(1, 100)
    page_1 = "https://taonet.siksikyuen.org.hk/images/StickEnquiry/stickPaper/{}.png".format(str(page))
    if context.args and len(context.args) != 0:
        await update.message.reply_text(
            "*Get a siksikyuen keifuk*\nUsage: `/siksikyuen`.", parse_mode='Markdown')
    else:
        await update.message.reply_photo(page_1, caption="https://taonet.siksikyuen.org.hk/StickEnquiry/{}/zh-TW".format(str(page)), parse_mode="Markdown")

handlers = [
    CommandHandler("senso", run_senso, block=False),
    CommandHandler("keifuk", run_keifuk, block=False)
]
