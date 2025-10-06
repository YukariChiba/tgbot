from telegram.ext import CommandHandler, ContextTypes
from telegram import Update

enabled = True


def load():
    print("ChatID Plugin Loaded!")


async def run(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "*Chat ID:* " + str(update.message.chat.id), parse_mode='Markdown')


handlers = [CommandHandler("chatid", run, block=False)]
