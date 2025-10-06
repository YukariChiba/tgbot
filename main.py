from dotenv import load_dotenv
import modules as bot_modules
from telegram.ext import Application
from utils.init import init, getEnvSafe
from telegram import Update

load_dotenv()

def main():
    application = Application.builder().token(getEnvSafe("BOTTOKEN")).build()
    for plugin in bot_modules.__all__:
        if plugin.enabled:
            plugin.load()
            for handler in plugin.handlers:
                application.add_handler(handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    init()
    main()
