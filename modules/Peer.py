from telegram.ext import ContextTypes, CommandHandler
from telegram import Update
import os
import re
from os import listdir
from os.path import isfile, join

from utils.init import getEnvSafe

enabled = True

node_pattern = re.compile("[A-Za-z0-9]+\\.[A-Za-z]+")


def load():
    print("Peer Plugin Loaded!")


async def listPeers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type == 'private':
        if len(context.args or []) == 0:
            peerfiles = [f.replace(".md", "") for f in listdir(getEnvSafe("MODULE_PEER_FILES")) if isfile(
                join(getEnvSafe("MODULE_PEER_FILES"), f)) and f != "README.md"]
            await update.message.reply_text(
                "*Node list*:\n\n" + "\n".join(peerfiles), parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "*Get peering node list for AS4242421331 / AS4242421332 in DN42.*\nUsage: `/peerlist`.\n_Private Chat Only_", parse_mode='Markdown')


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type == 'private':
        if context.args and len(context.args) == 1:
            arg = context.args[0]
            if node_pattern.fullmatch(arg) and len(arg) > 3 and len(arg) < 20:
                if os.path.isfile(getEnvSafe("MODULE_PEER_FILES") + arg.lower() + ".md"):
                    with open(getEnvSafe("MODULE_PEER_FILES") + arg.lower() + ".md", 'r') as file:
                        data = file.read()
                    await update.message.reply_text(
                        data, parse_mode='Markdown')
                else:
                    await update.message.reply_text(
                        '`Node Not Found.`', parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    '`Invalid argument.`', parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "*Get peer information for AS4242421331 / AS4242421332 in DN42.*\nUsage: `/peer {node}`.\n_Private Chat Only_\n_See /peerlist First!_", parse_mode='Markdown')


handlers = [CommandHandler("peer", run, block=False), CommandHandler(
    "peerlist", listPeers, block=False)]
