from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import ipaddress
import subprocess
import os
from datetime import timedelta, datetime
from utils.getProfilePhoto import getUserProfilePhoto
from PIL import Image, ImageDraw, ImageFont
import re
import emoji

username_pattern = re.compile("[A-Za-z0-9_]+")

baseImage = None

enabled = True


def load():
    global baseImage, baseBreedImage
    baseBreedImage = Image.open(os.getenv("MODULE_LOVE_BREEDBASEIMAGE"))
    baseImage = Image.open(os.getenv("MODULE_LOVE_BASEIMAGE"))
    print("Love Plugin Loaded!")


def validUsername(arg):
    return arg.startswith("@") and username_pattern.fullmatch(arg[1:]) and len(arg) > 4 and len(arg) < 17


def validArg(args):
    if len(args) == 1 and validUsername(args[0]):
        return True
    elif len(args) == 2 and validUsername(args[0]) and validUsername(args[1]):
        return True
    else:
        return False


def putRoundPhoto(base, user, pos):
    w, h = user.size
    alpha_layer = Image.new('L', (w, w), 0)
    draw = ImageDraw.Draw(alpha_layer)
    draw.ellipse((0, 0, w, w), fill=255)
    base.paste(user, pos, alpha_layer)


def putText(base, text, pos):
    font = ImageFont.truetype(os.getenv("MODULE_LOVE_TEXTFONT"), 36)
    draw = ImageDraw.Draw(base)
    w, h = draw.textsize(text, font=font)
    draw.text((pos[0]-w/2, pos[1]), text, font=font,
              stroke_fill="black", stroke_width=4)


def makeLove(user1, user2, imageType):
    global baseImage, baseBreedImage
    if imageType == 1:
        base = baseBreedImage.copy()
    else:
        base = baseImage.copy()
    user1Photo = Image.open(
        os.getenv("USER_PHOTO_STORE") + user1.lower()).resize((200, 200))
    user2Photo = Image.open(
        os.getenv("USER_PHOTO_STORE") + user2.lower()).resize((200, 200))
    putRoundPhoto(base, user1Photo, (140, 150))
    putRoundPhoto(base, user2Photo, (660, 150))
    draw = ImageDraw.Draw(base)
    putText(base, "@" + user1, (240, 380))
    putText(base, "@" + user2, (760, 380))
    base.save(os.getenv("MODULE_LOVE_TMP"), "WEBP")


def love(update: Update, context: CallbackContext) -> None:
    gen(update, context, 0)


def breed(update: Update, context: CallbackContext) -> None:
    gen(update, context, 1)


def gen(update: Update, context: CallbackContext, imageType: int) -> None:
    if not validArg(context.args):
        update.message.reply_text(
            emoji.emojize(":heart_with_arrow: *跟某人/让两人贴贴.*\nUsage: `/love {@someone} [@anotherone]`.\n_Alias:_ `/tie`"), parse_mode='Markdown')
    else:
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        if len(context.args) == 1:
            user1 = getUserProfilePhoto(
                update.message.from_user.username, context)
            user2 = getUserProfilePhoto(context.args[0][1:], context)
            user1id = update.message.from_user.username
            user2id = context.args[0][1:]
            if user2 == None or user1 == None:
                update.message.reply_text("坏掉了，可能是没照片。")
                return
        else:
            user1 = getUserProfilePhoto(context.args[0][1:], context)
            user2 = getUserProfilePhoto(context.args[1][1:], context)
            user1id = context.args[0][1:]
            user2id = context.args[1][1:]
            if user2 == None or user1 == None:
                update.message.reply_text("坏掉了，可能是没照片。")
                return
        makeLove(user1id, user2id, imageType)
        update.message.reply_sticker(
            open(os.getenv("MODULE_LOVE_TMP"), 'rb'))


handlers = [CommandHandler("love", love, run_async=True), CommandHandler(
    "tie", love, run_async=True), CommandHandler("breed", breed, run_async=True)]
