from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
import subprocess

enabled = True


def makeReplyMarkup(ip: str):
    keyboard = [
        [
            InlineKeyboardButton("TraceRoute", callback_data='/trace ' + ip)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def load():
    print("Ping Plugin Loaded!")


def exec_ping(ip: str, protocol: int=0):
    if protocol == 0:
        result = subprocess.run(['ping', '-c', '5', ip],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        result = subprocess.run(['ping', '-c', '5', '-' + str(protocol), ip],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.decode("utf-8") == "":
        return result.stderr.decode("utf-8")
    return result.stdout.decode("utf-8")


async def pingCallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await context.bot.sendChatAction(
        chat_id=query.message.chat_id, action=ChatAction.TYPING)
    ip = query.data.replace("/ping ", "")
    result = exec_ping(ip)
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text("```\n" + result + "\n```",
                             parse_mode='Markdown')


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "*Ping a host.*\nUsage: `/ping {IP}`.", parse_mode='Markdown')
    else:
        await context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_ping(context.args[0])
        await update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


async def ping4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "*Ping a host using IPv4.*\nUsage: `/ping4 {IP}`.", parse_mode='Markdown')
    else:
        await context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_ping(context.args[0], 4)
        await update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


async def ping6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "*Ping a host using IPv6.*\nUsage: `/ping6 {IP}`.", parse_mode='Markdown')
    else:
        await context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING)
        result = exec_ping(context.args[0], 6)
        await update.message.reply_text(
            "```\n" + result + "\n```", parse_mode='Markdown', reply_markup=makeReplyMarkup(context.args[0]))


handlers = [CommandHandler("ping", ping, block=False),
            CommandHandler("ping4", ping4, block=False),
            CommandHandler("ping6", ping6, block=False),
            CallbackQueryHandler(pingCallback, pattern='/ping *', block=False)]

if __name__ == "__main__":
    exec_ping("1.1.1.1")
