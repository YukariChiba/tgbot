from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import ipaddress
import subprocess
import os
import re
from os import listdir
from os.path import isfile, join

enabled = True

node_pattern = re.compile("[A-Za-z0-9]+\\.[A-Za-z]+")


def load():
    print("Peer Plugin Loaded!")


def listPeers(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        if len(context.args) == 0:
            peerfiles = [f.replace(".md", "") for f in listdir(os.getenv("MODULE_PEER_FILES")) if isfile(
                join(os.getenv("MODULE_PEER_FILES"), f)) and f != "README.md"]
            update.message.reply_text(
                "*Node list*:\n\n" + "\n".join(peerfiles), parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Get peering node list for AS4242421331 / AS4242421332 in DN42.*\nUsage: `/peerlist`.\n_Private Chat Only_", parse_mode='Markdown')


def run(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        if len(context.args) == 1:
            arg = context.args[0]
            if node_pattern.fullmatch(arg) and len(arg) > 3 and len(arg) < 20:
                if os.path.isfile(os.getenv("MODULE_PEER_FILES") + arg.lower() + ".md"):
                    with open(os.getenv("MODULE_PEER_FILES") + arg.lower() + ".md", 'r') as file:
                        data = file.read()
                    update.message.reply_text(
                        data, parse_mode='Markdown')
                else:
                    update.message.reply_text(
                        '`Node Not Found.`', parse_mode='Markdown')
            else:
                update.message.reply_text(
                    '`Invalid argument.`', parse_mode='Markdown')
        else:
            update.message.reply_text(
                "*Get peer information for AS4242421331 / AS4242421332 in DN42.*\nUsage: `/peer {node}`.\n_Private Chat Only_\n_See /peerlist First!_", parse_mode='Markdown')


handlers = [CommandHandler("peer", run, run_async=True), CommandHandler(
    "peerlist", listPeers, run_async=True)]
