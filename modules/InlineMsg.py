from telegram.ext import InlineQueryHandler, CallbackContext
from telegram import Update
import inlines as inline_plugins
import os

enabled = True

def load():
    for plugin in inline_plugins.__all__:
        if plugin.enabled:
            plugin.load()
    print("Inline Plugin Loaded!")

def run(update: Update, context: CallbackContext) -> None:
    query = update.inline_query
    results = [
    ]
    for plugin in inline_plugins.__all__:
        if plugin.enabled and plugin.filter(query.query):
            returnMessage = plugin.run(query, context)
            if returnMessage != None:
                results.append(returnMessage)
    update.inline_query.answer(results, cache_time=int(os.getenv("MODULE_INLINE_CACHETIME")), is_personal=True)

handlers = [InlineQueryHandler(run)]