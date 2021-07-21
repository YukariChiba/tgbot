from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
from mcstatus import MinecraftServer
import base64
enabled = True


def load():
    print("MCStatus Plugin Loaded!")


def args_check(args):
    if len(args) == 1 or len(args) == 2:
        if len(args) == 2:
            if not args[1].isnumeric():
                return False
            elif int(args[1]) > 65535 or int(args[1]) < 1:
                return False
        return True
    else:
        return False


def run(update: Update, context: CallbackContext) -> None:
    port = 25565
    if args_check(context.args):
        if len(context.args) == 2:
            port = int(context.args[1])
        server = MinecraftServer.lookup("{}:{}".format(context.args[0], port))
        try:
            context.bot.sendChatAction(
                chat_id=update.message.chat_id, action=ChatAction.TYPING)
            query = server.query()
            status = server.status()
            if status.favicon:
                favicon_image = base64.b64decode(
                    status.favicon.replace("data:image/png;base64,", ""))
                update.message.reply_photo(favicon_image, caption="Status for `{}`\n*Version*: `{} - {}`\n*MOTD*: `{}`\n*Players*: `{}`".format(
                    "{}:{}".format(context.args[0], port), query.software.brand, query.software.version, query.motd, ", ".join(query.players.names)),  parse_mode='Markdown')
            else:
                update.message.reply_text("Status for `{}`\n*Version*: `{} - {}`\n*MOTD*: `{}`\n*Players*: `{}`".format(
                    "{}:{}".format(context.args[0], port), query.software.brand, query.software.version, query.motd, ", ".join(query.players.names)),  parse_mode='Markdown')
        except:
            try:
                status = server.status()
                if status.favicon:
                    favicon_image = base64.b64decode(
                        status.favicon.replace("data:image/png;base64,", ""))
                    update.message.reply_photo(favicon_image, caption="Status for `{}`\n*Version*: `{}`\n*Players*: `{}/{}`".format(
                        "{}:{}".format(context.args[0], port), status.version.name, status.players.online, status.players.max),  parse_mode='Markdown')
                else:
                    update.message.reply_text("Status for `{}`\n*Version*: `{}`\n*Players*: `{}/{}`".format(
                        "{}:{}".format(context.args[0], port), status.version.name, status.players.online, status.players.max),  parse_mode='Markdown')
            except:
                update.message.reply_text(
                    "`Server Error.`", parse_mode='Markdown')
    else:
        update.message.reply_text(
            "*Get the status of Minecraft server.*\nUsage: `/mcstatus <Server> [Port]`.", parse_mode='Markdown')


handlers = [CommandHandler("mcstatus", run, run_async=True)]
