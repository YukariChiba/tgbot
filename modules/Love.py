from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
from telegram.constants import ChatAction
from utils.getProfilePhoto import getUserProfilePhoto
from PIL import Image, ImageDraw, ImageFont
import re
import emoji

from utils.init import getEnvSafe

username_pattern = re.compile("[A-Za-z0-9_]+")

baseImage = None

enabled = True


def load():
    from utils.init import chk_dir
    chk_dir(getEnvSafe("CACHE_DIR") + "tmp/Love")
    global baseImage, baseBreedImage
    baseBreedImage = Image.open(getEnvSafe("MODULE_LOVE_BREEDBASEIMAGE"))
    baseImage = Image.open(getEnvSafe("MODULE_LOVE_BASEIMAGE"))
    print("Love Plugin Loaded!")

def validUsername(arg: str):
    return arg.startswith("@") and username_pattern.fullmatch(arg[1:]) and len(arg) > 4 and len(arg) < 17

def validArg(args: list[str]):
    if len(args) == 1 and validUsername(args[0]):
        return True
    elif len(args) == 2 and validUsername(args[0]) and validUsername(args[1]):
        return True
    else:
        return False


def putRoundPhoto(base: Image.Image, user: Image.Image, pos: tuple[int, int]):
    w, _ = user.size
    alpha_layer = Image.new('L', (w, w), 0)
    draw = ImageDraw.Draw(alpha_layer)
    draw.ellipse((0, 0, w, w), fill=255)
    base.paste(user, pos, alpha_layer)

def putText(base: Image.Image, text: str, pos: tuple[int, int]):
    font = ImageFont.truetype(getEnvSafe("MODULE_LOVE_TEXTFONT"), 36)
    draw = ImageDraw.Draw(base)
    w = draw.textlength(text, font=font)
    draw.text((pos[0]-w/2, pos[1]), text, font=font,
              stroke_fill="black", stroke_width=4)

def makeLove(user1: str, user2: str, imageType: int):
    global baseImage, baseBreedImage
    if imageType == 1:
        base = baseBreedImage.copy()
    else:
        base = baseImage.copy()
    user1Photo = Image.open(
        getEnvSafe("CACHE_DIR") + "user_photo/" + user1.lower()).resize((200, 200))
    user2Photo = Image.open(
        getEnvSafe("CACHE_DIR") + "user_photo/" + user2.lower()).resize((200, 200))
    putRoundPhoto(base, user1Photo, (140, 150))
    putRoundPhoto(base, user2Photo, (660, 150))
    putText(base, "@" + user1, (240, 380))
    putText(base, "@" + user2, (760, 380))
    base.save(getEnvSafe("CACHE_DIR") + "tmp/Love/love.webp", "WEBP")


async def love(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await gen(update, context, 0)


async def breed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await gen(update, context, 1)


async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE, imageType: int) -> None:
    if not context.args or not validArg(context.args):
        await update.message.reply_text(
            emoji.emojize(":heart_with_arrow: *跟某人/让两人贴贴.*\nUsage: `/love {@someone} [@anotherone]`.\n_Alias:_ `/tie`"), parse_mode='Markdown')
    else:
        await context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        if len(context.args) == 1:
            if not update.message.from_user.username:
                await update.message.reply_text("坏掉了，可能是没照片。")
                return
            user1 = getUserProfilePhoto(
                update.message.from_user.username)
            user2 = getUserProfilePhoto(context.args[0][1:])
            user1id = update.message.from_user.username
            user2id = context.args[0][1:]
            if user2 == None or user1 == None:
                await update.message.reply_text("坏掉了，可能是没照片。")
                return
        else:
            user1 = getUserProfilePhoto(context.args[0][1:])
            user2 = getUserProfilePhoto(context.args[1][1:])
            user1id = context.args[0][1:]
            user2id = context.args[1][1:]
            if user2 == None or user1 == None:
                await update.message.reply_text("坏掉了，可能是没照片。")
                return
        makeLove(user1id, user2id, imageType)
        await update.message.reply_sticker(
            open(getEnvSafe("CACHE_DIR") + "tmp/Love/love.webp", 'rb'))


handlers = [CommandHandler("love", love, block=False), CommandHandler(
    "tie", love, block=False), CommandHandler("breed", breed, block=False)]
