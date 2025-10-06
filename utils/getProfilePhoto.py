import os
from datetime import timedelta, datetime, timezone
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
from utils.init import getEnvSafe

def validFile(file: str, delta: timedelta):
    cutoff = datetime.now(timezone.utc) - delta
    mtime = datetime.fromtimestamp(os.path.getmtime(file), timezone.utc)
    if mtime < cutoff:
        return False
    return True

def getUserProfilePhoto(user: str):
    file_id = getEnvSafe("CACHE_DIR") + "user_photo/" + user.lower()
    if not os.path.isfile(file_id) or not validFile(file_id, timedelta(days=int(getEnvSafe("USER_PHOTO_VALID_DAYS")))):
        bs = BS(urlopen("https://t.me/" + user), 'html.parser')
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
