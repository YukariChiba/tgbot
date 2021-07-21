from pathlib import Path

def chk_dir(dir):
    Path(dir).mkdir(parents=True, exist_ok=True)

def init():
    chk_dir(os.getenv("CACHE_DIR"))
    chk_dir(os.getenv("CACHE_DIR") + "/tmp")
    chk_dir(os.getenv("CACHE_DIR") + "/user_photo")
