from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction
from telegram.utils.helpers import escape_markdown
import os
from datetime import timedelta, datetime
from utils.getProfilePhoto import getUserProfilePhoto
from PIL import Image, ImageDraw, ImageFont
from utils.wrapTextImage import fitText
from utils.userInfo import getUserName
import emoji
from pilmoji import Pilmoji

enabled = True

CENTER_POS = 820

TEXT_SIZE_EXLARGE = 56
TEXT_SIZE_LARGE = 48
TEXT_SIZE = 42
USER_SIZE = 28
CODE_SIZE = 20


def load():
    from utils.init import chk_dir
    chk_dir(os.getenv("CACHE_DIR") + "tmp/MakeQuote")
    global baseImage
    baseImage = Image.open(os.getenv("MODULE_MAKEQUOTE_BASEIMAGE"))
    print("MakeQuote Plugin Loaded!")


def putText(base, text, pos, font_size, font_type, color=None):
    useFont = ImageFont.truetype(font_type, font_size)
    if text == "":
        _, h = base.getsize("demo", font=useFont)
        return h
    w, h = base.getsize(text, font=useFont)
    base.text((pos[0] - w//2, pos[1]), text,
              fill=color,
              font=useFont, embedded_color=True,            emoji_scale_factor=0.8,
              emoji_position_offset=(0, font_size//2))
    return h


def putTexts(base, text_msg, text_user, text_userid):
    currentTextSize = TEXT_SIZE
    draw = Pilmoji(base)
    lines = 0
    textFont = ImageFont.truetype(os.getenv("MODULE_MAKEQUOTE_TEXTFONT"), currentTextSize)
    texts = fitText(draw, textFont, text_msg, 640, 500)
    len_texts = len(texts.split('\n'))

    # Scaling, need recalc
    if(len_texts < 4):
        if(len_texts < 2):
            currentTextSize = TEXT_SIZE_EXLARGE
        else:
            currentTextSize = TEXT_SIZE_LARGE
        textFont = ImageFont.truetype(os.getenv("MODULE_MAKEQUOTE_TEXTFONT"), currentTextSize)
        texts = fitText(draw, textFont, text_msg, 640, 500)
        len_texts = len(texts.split('\n'))

    remaining_start = 270 - (currentTextSize * len_texts + 4) // 2
    cnt = 0
    for text in texts.split('\n'):
        remaining_start = remaining_start + putText(
            draw,
            text,
            (CENTER_POS, remaining_start),
            currentTextSize,
            os.getenv("MODULE_MAKEQUOTE_TEXTFONT")
        ) + 4

    remaining_start = remaining_start + currentTextSize // 2

    remaining_start = remaining_start + putText(
        draw,
        text_user,
        (CENTER_POS, remaining_start),
        USER_SIZE,
        os.getenv("MODULE_MAKEQUOTE_USERFONT")
    ) + 4

    remaining_start = remaining_start + USER_SIZE // 2

    remaining_start = remaining_start + putText(
        draw,
        text_userid,
        (CENTER_POS, remaining_start),
        CODE_SIZE,
        os.getenv("MODULE_MAKEQUOTE_CODEFONT"),
        color="gray"
    )


def makeQuoteGen(user, usertext, text):
    global baseImage, baseFont, userFont
    base = baseImage.copy()
    userPhoto = Image.open(
        os.getenv("CACHE_DIR") + "user_photo/" + user.lower()).resize((630, 630))
    userPhotoFull = Image.new('RGBA', base.size, color=0)
    userPhotoFull.paste(userPhoto, (-40, 0))
    base = Image.alpha_composite(userPhotoFull, base)
    putTexts(base, text, "— " + usertext, "@" + user)
    base.save(os.getenv("CACHE_DIR") + "tmp/MakeQuote/generated.png", "PNG")


def makeQuote(update: Update, context: CallbackContext) -> None:
    reply_to = update.message.reply_to_message
    if not reply_to:
        update.message.reply_text(
            emoji.emojize("*Generate quote image for replied message.*\nUsage: `/makequote`."), parse_mode='Markdown')
    elif not reply_to.text:
        update.message.reply_text(
            emoji.emojize("`Error: No valid text.`"), parse_mode='Markdown')
    else:
        if reply_to.forward_from:
            username = reply_to.forward_from.username
            username_text = getUserName(reply_to.forward_from)
        else:
            username = reply_to.from_user.username
            username_text = getUserName(reply_to.from_user)
        if username == None:
            update.message.reply_text("No username found.")
            return
        context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        user = getUserProfilePhoto(username, context)
        if user == None:
            update.message.reply_text("No profile photo found.")
            return
        try:
            makeQuoteGen(username, username_text, reply_to.text)
            update.message.reply_photo(
                open(os.getenv("CACHE_DIR") + "tmp/MakeQuote/generated.png", 'rb'))
        except Exception as e:
            print(e)
            update.message.reply_text("Message too long.")
            return


handlers = [CommandHandler("makequote", makeQuote, run_async=True)]
