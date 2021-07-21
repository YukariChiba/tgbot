from pathlib import Path

def chk_dir(dir):
    Path(dir).mkdir(parents=True, exist_ok=True)

def init():
    chk_dir("cache")
    chk_dir("cache/tmp")
    chk_dir("cache/user_photo")
