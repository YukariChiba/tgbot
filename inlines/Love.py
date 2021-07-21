from pathlib import Path
import os
from telegram import InlineQueryResultCachedSticker, InputTextMessageContent
from uuid import uuid4
import random
import requests
from datetime import timedelta, datetime
from utils.getProfilePhoto import getUserProfilePhoto
from utils.imageUpload import upload
from PIL import Image, ImageDraw, ImageFont
import re

enabled = True

username_pattern = re.compile("[A-Za-z0-9_]+")


def validUsername(arg):
    return arg.startswith("@") and username_pattern.fullmatch(arg[1:]) and len(arg) > 4 and len(arg) < 17


def load():
    global baseImage
    baseImage = Image.open(os.getenv("MODULE_LOVE_BASEIMAGE"))
    print("Love Inline Plugin Loaded!")


def filter(arg):
    if validUsername(arg):
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


def makeLove(user1, user2):
    global baseImage
    user1Photo = Image.open(
        os.getenv("CACHE_DIR") + "user_photo/" + user1.lower()).resize((200, 200))
    user2Photo = Image.open(
        os.getenv("CACHE_DIR") + "user_photo/" + user2.lower()).resize((200, 200))
    base = baseImage.copy()
    putRoundPhoto(base, user1Photo, (140, 150))
    putRoundPhoto(base, user2Photo, (660, 150))
    draw = ImageDraw.Draw(base)
    putText(base, "@" + user1, (240, 380))
    putText(base, "@" + user2, (760, 380))
    base.save(os.getenv("CACHE_DIR") + "tmp/Love/love_inline.webp", "WEBP")


def run(querybody, context):
    user1 = getUserProfilePhoto(
        querybody.from_user.username, context)
    user2 = getUserProfilePhoto(
        querybody.query[1:], context)
    user1id = querybody.from_user.username
    user2id = querybody.query[1:]
    if user2 == None or user1 == None:
        return None
    im = makeLove(user1id, user2id)
    file_upload = upload(os.getenv("CACHE_DIR") + "tmp/Love/love_inline.webp", context.bot)
    return_val = InlineQueryResultCachedSticker(
        id=uuid4(), sticker_file_id=file_upload)
    return return_val
