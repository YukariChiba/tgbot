import os

def upload(file, bot):
    infophoto = bot.sendSticker(chat_id=os.getenv("IMAGE_UPLOAD_CHANNELID"),sticker=open(file,'rb'))
    return infophoto["sticker"]["file_id"]
