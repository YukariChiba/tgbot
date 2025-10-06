from utils.init import getEnvSafe

async def upload(file, bot):
    infophoto = await bot.sendSticker(chat_id=getEnvSafe("IMAGE_UPLOAD_CHANNELID"),sticker=open(file,'rb'))
    return infophoto["sticker"]["file_id"]
