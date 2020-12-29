from dotenv import load_dotenv
import os
import modules as bot_modules
from telegram.ext import Updater

load_dotenv()

def main():
    updater = Updater(os.getenv("BOTTOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    for plugin in bot_modules.__all__:
        if plugin.enabled:
            plugin.load()
            for handler in plugin.handlers:
                dispatcher.add_handler(handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()