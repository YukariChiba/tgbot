import os

def chk_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def init():
    chk_dir("cache")
    chk_dir("cache/tmp")
    chk_dir("cache/user_photo")