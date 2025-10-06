from telegram.ext import CommandHandler, ContextTypes
from telegram import Update

enabled = True


def load():
    print("Mie Plugin Loaded!")

async def run(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("咩～")


handlers = [CommandHandler("mie", run, block=False)]
