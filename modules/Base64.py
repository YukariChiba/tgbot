from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
import base64

enabled = True


def load():
    print("Base64 Plugin Loaded!")

async def _help_de(update: Update):
    await update.message.reply_text(
            "*Base64 decode.*\nUsage: `/b64de [code]`.", parse_mode='Markdown')

async def _help_en(update: Update):
    await update.message.reply_text(
            "*Base64 encode.*\nUsage: `/b64en <text>`.", parse_mode='Markdown')

async def run_de(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = update.message.reply_to_message
    if context.args and len(context.args) == 1:
        if len(context.args[0]) < 120:
            try:
                await update.message.reply_text("Base64 decode result:\n`{}`".format(base64.b64decode(context.args[0]).decode()), parse_mode='Markdown')
            except:
                await update.message.reply_text(
                    "`Error: Invalid code.`", parse_mode='Markdown')
        else:
            await update.message.reply_text(
                    "`Error: Code too long.`", parse_mode='Markdown')
    elif reply_message and len(context.args or []) == 0:
        if reply_message.text and len(reply_message.text) < 50:
            try:
                await update.message.reply_text("Base64 decode result:\n`{}`".format(base64.b64decode(reply_message.text).decode()), parse_mode='Markdown')
            except:
                await update.message.reply_text(
                    "`Error: Invalid code.`", parse_mode='Markdown')
        else:
            await update.message.reply_text(
                    "`Error: Code too long or invalid.`", parse_mode='Markdown')
    else:
        await _help_de(update)

async def run_en(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = update.message.reply_to_message
    if context.args and len(context.args) >= 1:
        txt = " ".join(context.args)
        if len(txt) < 50:
            await update.message.reply_text("Base64 encode result:\n`{}`".format(base64.b64encode(str.encode(txt)).decode()), parse_mode='Markdown')
        else:
            await update.message.reply_text(
                    "`Error: Message too long.`", parse_mode='Markdown')
    elif reply_message and len(context.args or []) == 0:
        if reply_message.text and len(reply_message.text) < 50:
            await update.message.reply_text("Base64 encode result:\n`{}`".format(base64.b64encode(str.encode(reply_message.text)).decode()), parse_mode='Markdown')
        else:
            await update.message.reply_text(
                    "`Error: Message too long or invalid.`", parse_mode='Markdown')
    else:
        await _help_en(update)


handlers = [CommandHandler("b64en", run_en, block=False), CommandHandler("b64de", run_de, block=False)]
