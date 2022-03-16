from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import ipaddress
import subprocess
import os

enabled = True


def makeReplyMarkup(ip):
    keyboard = [
        [
            InlineKeyboardButton("Ping", callback_data='/ping ' + ip)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def load():
    print("Traceroute Plugin Loaded!")


def exec_trace(ip, protocol=0):
    if protocol == 0:
        result = subprocess.run(
            [os.getenv("MODULE_TRACE_BIN"), '-I', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        result = subprocess.run([os.getenv("MODULE_TRACE_BIN"), '-I', '-' + str(protocol), ip],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.decode("utf-8") == "":
        return result.stderr.decode("utf-8")
    return result.stdout.decode("utf-8")


def traceCallback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    context.bot.sendChatAction(
        chat_id=query.message.chat_id, action=ChatAction.TYPING)
    ip = query.data.replace("/trace ", "")
    result = exec_trace(ip)
    query.edit_message_reply_markup(reply_markup=None)
    query.message.reply_text("```\n" + result + "\n```",
                             parse_mode='Markdown')


def trace(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text(
            "*Traceroute to a host.*\nUsage: `/trace {IP}`.", parse_mode='Markdown')
    else:
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_trace(context.args[0])
        update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


def trace4(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text(
            "*Traceroute to a host using IPv4.*\nUsage: `/trace4 {IP}`.", parse_mode='Markdown')
    else:
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_trace(context.args[0], 4)
        update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


def trace6(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text(
            "*Traceroute to a host using IPv6.*\nUsage: `/trace6 {IP}`.", parse_mode='Markdown')
    else:
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_trace(context.args[0], 6)
        update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


handlers = [CommandHandler("trace", trace, run_async=True),
            CommandHandler("trace4", trace4, run_async=True),
            CommandHandler("trace6", trace6, run_async=True),
            CallbackQueryHandler(traceCallback, pattern='/trace *', run_async=True)]

if __name__ == "__main__":
    exec_trace("1.1.1.1")
