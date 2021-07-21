from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
import ipaddress
import subprocess
import os
from datetime import timedelta, datetime
from bs4 import BeautifulSoup as BS
from urllib.request import urlretrieve, urlopen


def validFile(file, delta):
    cutoff = datetime.utcnow() - delta
    mtime = datetime.utcfromtimestamp(os.path.getmtime(file))
    if mtime < cutoff:
        return False
    return True

def getUserProfilePhoto(user, context):
    file_id = os.getenv("CACHE_DIR") + "user_photo/" + user.lower()
    if not os.path.isfile(file_id) or validFile(file_id, timedelta(days=int(os.getenv("USER_PHOTO_VALID_DAYS")))):
        site = "https://t.me/" + user
        html = urlopen(site)
        bs = BS(html, 'html.parser')   
        image = bs.find("img", {"class": "tgme_page_photo_image"})
        if image == None:
            return None
        else:
            try:
                request = urlopen(image['src'], timeout=5)
                with open(file_id, 'wb') as f:
                        f.write(request.read())
            except:
                return None
    return True
