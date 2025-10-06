from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
import subprocess

from utils.init import getEnvSafe

enabled = True


def makeReplyMarkup(ip: str):
    keyboard = [
        [
            InlineKeyboardButton("Ping", callback_data='/ping ' + ip)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def load():
    print("Traceroute Plugin Loaded!")


def exec_trace(ip: str, protocol: int=0):
    if protocol == 0:
        result = subprocess.run(
            [getEnvSafe("MODULE_TRACE_BIN"), '-I', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        result = subprocess.run([getEnvSafe("MODULE_TRACE_BIN"), '-I', '-' + str(protocol), ip],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.decode("utf-8") == "":
        return result.stderr.decode("utf-8")
    return result.stdout.decode("utf-8")


async def traceCallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await context.bot.sendChatAction(
        chat_id=query.message.chat_id, action=ChatAction.TYPING)
    ip = query.data.replace("/trace ", "")
    result = exec_trace(ip)
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text("```\n" + result + "\n```",
                             parse_mode='Markdown')


async def trace(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "*Traceroute to a host.*\nUsage: `/trace {IP}`.", parse_mode='Markdown')
    else:
        await context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_trace(context.args[0])
        await update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


async def trace4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "*Traceroute to a host using IPv4.*\nUsage: `/trace4 {IP}`.", parse_mode='Markdown')
    else:
        await context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_trace(context.args[0], 4)
        await update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


async def trace6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "*Traceroute to a host using IPv6.*\nUsage: `/trace6 {IP}`.", parse_mode='Markdown')
    else:
        await context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_trace(context.args[0], 6)
        await update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


handlers = [CommandHandler("trace", trace, block=False),
            CommandHandler("trace4", trace4, block=False),
            CommandHandler("trace6", trace6, block=False),
            CallbackQueryHandler(traceCallback, pattern='/trace *', block=False)]

if __name__ == "__main__":
    exec_trace("1.1.1.1")
