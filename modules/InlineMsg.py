from telegram.ext import InlineQueryHandler, ContextTypes
from telegram import Update
import inlines as inline_plugins

from utils.init import getEnvSafe

enabled = True


def load():
    for plugin in inline_plugins.__all__:
        if plugin.enabled:
            plugin.load()
    print("Inline Plugin Loaded!")


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query
    results = [
    ]
    cache_time = int(getEnvSafe("MODULE_INLINE_CACHETIME"))
    for plugin in inline_plugins.__all__:
        if plugin.enabled and plugin.filter(query.query):
            returnMessage = plugin.run(query, context)
            if returnMessage != None:
                if hasattr(plugin, 'NOCACHE'):
                    cache_time = 0
                results.append(returnMessage)
    await update.inline_query.answer(
        results, cache_time=cache_time, is_personal=True)


handlers = [InlineQueryHandler(run, block=False)]
