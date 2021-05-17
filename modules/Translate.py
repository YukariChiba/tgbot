from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
from googletrans import Translator

enabled = True

translator = None


def load():
    global translator
    translator = Translator()
    print("Translate Plugin Loaded!")


def run(update: Update, context: CallbackContext) -> None:
    global translator
    reply_message = update.message.reply_to_message
    if reply_message and len(context.args) <= 1:
        if reply_message.text:
            if len(reply_message.text) < 500:
                dest = "zh-CN"
                if len(context.args) == 1:
                    dest = context.args[0]
                try:
                    result = translator.translate(
                        reply_message.text, dest=dest)
                    update.message.reply_text("Translate from `{0}` to `{1}`: \n\n{2}".format(
                        result.src, result.dest, result.text), parse_mode='Markdown')
                except ValueError:
                    update.message.reply_text(
                        "`Error: Invalid language code.`", parse_mode='Markdown')
            else:
                update.message.reply_text(
                    "`Error: Message too long.`", parse_mode='Markdown')
        else:
            update.message.reply_text(
                "`Error: No text found.`", parse_mode='Markdown')
    else:
        update.message.reply_text(
            "*Translate the replied message.*\nUsage: `/trans [lang_code]`.", parse_mode='Markdown')


handlers = [CommandHandler("trans", run, run_async=True), CommandHandler(
    "translate", run, run_async=True)]
