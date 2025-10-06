from telegram.ext import ContextTypes, CommandHandler
from telegram import Update
from telegram.constants import ChatAction
from mcstatus import JavaServer as MinecraftServer
import base64
enabled = True


def load():
    print("MCStatus Plugin Loaded!")


def args_check(args: list[str]):
    if len(args) == 1 or len(args) == 2:
        if len(args) == 2:
            if not args[1].isnumeric():
                return False
            elif int(args[1]) > 65535 or int(args[1]) < 1:
                return False
        return True
    else:
        return False


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    port = 25565
    if context.args and args_check(context.args):
        if len(context.args) == 2:
            port = int(context.args[1])
        server = MinecraftServer.lookup("{}:{}".format(context.args[0], port))
        try:
            await context.bot.sendChatAction(
                chat_id=update.message.chat_id, action=ChatAction.TYPING)
            query = server.query()
            status = server.status()
            if status.favicon:
                favicon_image = base64.b64decode(
                    status.favicon.replace("data:image/png;base64,", ""))
                await update.message.reply_photo(favicon_image, caption="Status for `{}`\n*Version*: `{} - {}`\n*MOTD*: `{}`\n*Players*: `{}`".format(
                    "{}:{}".format(context.args[0], port), query.software.brand, query.software.version, query.motd, ", ".join(query.players.names)),  parse_mode='Markdown')
            else:
                await update.message.reply_text("Status for `{}`\n*Version*: `{} - {}`\n*MOTD*: `{}`\n*Players*: `{}`".format(
                    "{}:{}".format(context.args[0], port), query.software.brand, query.software.version, query.motd, ", ".join(query.players.names)),  parse_mode='Markdown')
        except:
            try:
                status = server.status()
                if status.favicon:
                    favicon_image = base64.b64decode(
                        status.favicon.replace("data:image/png;base64,", ""))
                    await update.message.reply_photo(favicon_image, caption="Status for `{}`\n*Version*: `{}`\n*Players*: `{}/{}`".format(
                        "{}:{}".format(context.args[0], port), status.version.name, status.players.online, status.players.max),  parse_mode='Markdown')
                else:
                    await update.message.reply_text("Status for `{}`\n*Version*: `{}`\n*Players*: `{}/{}`".format(
                        "{}:{}".format(context.args[0], port), status.version.name, status.players.online, status.players.max),  parse_mode='Markdown')
            except:
                await update.message.reply_text(
                    "`Server Error.`", parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "*Get the status of Minecraft server.*\nUsage: `/mcstatus <Server> [Port]`.", parse_mode='Markdown')


handlers = [CommandHandler("mcstatus", run, block=False)]
