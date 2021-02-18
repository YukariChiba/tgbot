from dotenv import load_dotenv
import os
import modules as bot_modules
import schedules as bot_schedules
from utils.init import init
from telegram.ext import Updater

load_dotenv()

def main():
    updater = Updater(os.getenv("BOTTOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    queue = updater.job_queue
    for plugin in bot_modules.__all__:
        if plugin.enabled:
            plugin.load()
            for handler in plugin.handlers:
                dispatcher.add_handler(handler)
    for schedule in bot_schedules.__all__:
        if schedule.enabled:
            schedule.load()
            for job in schedule.jobs:
                queue.run_repeating(job["callback"], interval=job["interval"], first=job["first"])
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    init()
    main()
