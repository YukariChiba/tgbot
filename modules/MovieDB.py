from telegram.ext import ContextTypes, CommandHandler
from telegram import Update
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


async def run_tv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global tmdb
    arg = " ".join(context.args or [])
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
            returnText = returnText + \
                "[TMDB Link](https://www.themoviedb.org/tv/{0})".format(
                    show.id)
            if show.poster_path:
                await update.message.reply_photo(
                    tmdb_base_url + show.poster_path, caption=returnText, parse_mode='Markdown')
            else:
                await update.message.reply_text(returnText, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "`Error: Not Found`", parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "*Search for a TV series.*\nUsage: `/tvseries {TV series name}`.", parse_mode='Markdown')


async def run_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global tmdb
    arg = " ".join(context.args or [])
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
            returnText = returnText + \
                "[TMDB Link](https://www.themoviedb.org/movie/{0})".format(
                    mv.id)
            if mv.poster_path:
                await update.message.reply_photo(
                    tmdb_base_url + mv.poster_path, caption=returnText, parse_mode='Markdown')
            else:
                await update.message.reply_text(returnText, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "`Error: Not Found`", parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "*Search for a movie.*\nUsage: `/movie {movie name}`.", parse_mode='Markdown')


handlers = [CommandHandler("tvseries", run_tv, block=False),
            CommandHandler("movie", run_movie, block=False)]
