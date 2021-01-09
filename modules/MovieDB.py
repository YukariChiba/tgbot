from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
from tmdbv3api import TMDb, Movie, TV
import os

enabled = True

tmdb = TMDb()

tmdb_base_url = "https://image.tmdb.org/t/p/w500"


def load():
    global tmdb
    tmdb.api_key = os.getenv("MODULE_TMDB_KEY")
    tmdb.language = os.getenv("MODULE_TMDB_LANG")
    print("MovieDB Plugin Loaded!")


def run_tv(update: Update, context: CallbackContext) -> None:
    global tmdb
    arg = " ".join(context.args)
    if len(arg) >= 1 and len(arg) <= 40:
        tv = TV()
        show = tv.search(arg)
        if len(show) > 0:
            show = show[0]
            returnText = "*Title*: {0}\n".format(show.name)
            if show.overview:
                returnText = returnText + \
                    "*Overview*: {0}\n".format(show.overview)
            if show.first_air_date:
                returnText = returnText + \
                    "*Date*: {0}\n".format(show.first_air_date)
            if show.poster_path:
                update.message.reply_photo(
                    tmdb_base_url + show.poster_path, caption=returnText, parse_mode='Markdown')
            else:
                update.message.reply_text(returnText, parse_mode='Markdown')
        else:
            update.message.reply_text(
                "`Error: Not Found`", parse_mode='Markdown')
    else:
        update.message.reply_text(
            "*Search for a TV series.*\nUsage: `/tvseries {TV series name}`.", parse_mode='Markdown')


def run_movie(update: Update, context: CallbackContext) -> None:
    global tmdb
    arg = " ".join(context.args)
    if len(arg) >= 1 and len(arg) <= 40:
        movie = Movie()
        mv = movie.search(arg)
        if len(mv) > 0:
            mv = mv[0]
            returnText = "*Title*: {0}\n".format(mv.title)
            if mv.overview:
                returnText = returnText + \
                    "*Overview*: {0}\n".format(mv.overview)
            if mv.release_date:
                returnText = returnText + \
                    "*Date*: {0}\n".format(mv.release_date)
            if mv.poster_path:
                update.message.reply_photo(
                    tmdb_base_url + mv.poster_path, caption=returnText, parse_mode='Markdown')
            else:
                update.message.reply_text(returnText, parse_mode='Markdown')
        else:
            update.message.reply_text(
                "`Error: Not Found`", parse_mode='Markdown')
    else:
        update.message.reply_text(
            "*Search for a movie.*\nUsage: `/tvseries {movie name}`.", parse_mode='Markdown')


handlers = [CommandHandler("tvseries", run_tv),
            CommandHandler("movie", run_movie)]
