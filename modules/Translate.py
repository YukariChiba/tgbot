from telegram.ext import ContextTypes, CommandHandler
from telegram import Update
from googletrans import Translator

enabled = True

translator = None


def load():
    global translator
    translator = Translator()
    print("Translate Plugin Loaded!")


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global translator
    reply_message = update.message.reply_to_message
    if context.args and reply_message and len(context.args) <= 1:
        if reply_message.text:
            if len(reply_message.text) < 500:
                dest = "zh-CN"
                if len(context.args) == 1:
                    dest = context.args[0]
                try:
                    result = translator.translate(
                        reply_message.text, dest=dest)
                    await update.message.reply_text("Translate from `{0}` to `{1}`: \n\n{2}".format(
                        result.src, result.dest, result.text), parse_mode='Markdown')
                except ValueError:
                    await update.message.reply_text(
                        "`Error: Invalid language code.`", parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "`Error: Message too long.`", parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "`Error: No text found.`", parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "*Translate the replied message.*\nUsage: `/trans [lang_code]`.", parse_mode='Markdown')


handlers = [CommandHandler("trans", run, block=False), CommandHandler(
    "translate", run, block=False)]
