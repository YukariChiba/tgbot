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
            InlineKeyboardButton("TraceRoute", callback_data='/trace ' + ip)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def load():
    print("Ping Plugin Loaded!")


def exec_ping(ip, protocol=0):
    if protocol == 0:
        result = subprocess.run(['ping', '-c', '5', ip],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        result = subprocess.run(['ping', '-c', '5', '-' + str(protocol), ip],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.decode("utf-8") == "":
        return result.stderr.decode("utf-8")
    return result.stdout.decode("utf-8")


def pingCallback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    context.bot.sendChatAction(
        chat_id=query.message.chat_id, action=ChatAction.TYPING)
    ip = query.data.replace("/ping ", "")
    result = exec_ping(ip)
    query.edit_message_reply_markup(reply_markup=None)
    query.message.reply_text("```\n" + result + "\n```",
                             parse_mode='Markdown')


def ping(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text(
            "*Ping a host.*\nUsage: `/ping {IP}`.", parse_mode='Markdown')
    else:
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_ping(context.args[0])
        update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


def ping4(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text(
            "*Ping a host using IPv4.*\nUsage: `/ping4 {IP}`.", parse_mode='Markdown')
    else:
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_ping(context.args[0], 4)
        update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


def ping6(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text(
            "*Ping a host using IPv6.*\nUsage: `/ping6 {IP}`.", parse_mode='Markdown')
    else:
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_ping(context.args[0], 6)
        update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


handlers = [CommandHandler("ping", ping, run_async=True),
            CommandHandler("ping4", ping4, run_async=True),
            CommandHandler("ping6", ping6, run_async=True),
            CallbackQueryHandler(pingCallback, pattern='/ping *', run_async=True)]

if __name__ == "__main__":
    exec_ping("1.1.1.1")
