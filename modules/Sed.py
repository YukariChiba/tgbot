from telegram.ext import ContextTypes, CommandHandler
from telegram import Update
import re

enabled = True


def load():
    print("Sed Plugin Loaded!")


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = update.message.reply_to_message
    if reply_message and context.args and len(context.args) == 2:
        if reply_message.text:
            if len(context.args[0]) < 18 and len(context.args[1]) < 18:
                replaced_text = re.sub(
                    context.args[0], context.args[1], reply_message.text)
                if len(replaced_text) < 500:
                    await update.message.reply_text("Replace `{0}` with `{1}`: \n\n{2}".format(
                        context.args[0], context.args[1], replaced_text), parse_mode='Markdown')
                else:
                    await update.message.reply_text(
                        "`Error: Result too long.`", parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "`Error: Keyword too long.`", parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "`Error: No text found.`", parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "*Sed to the replied message.*\nUsage: `/sed {from_regex} {to_regex}`.", parse_mode='Markdown')


handlers = [CommandHandler("sed", run, block=False)]
