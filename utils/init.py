from pathlib import Path
import os

def getEnvSafe(env: str):
    ret = os.getenv(env)
    assert ret != None
    return ret

def chk_dir(dir: str):
    Path(dir).mkdir(parents=True, exist_ok=True)

def init():
    chk_dir(getEnvSafe("CACHE_DIR"))
    chk_dir(getEnvSafe("CACHE_DIR") + "/tmp")
    chk_dir(getEnvSafe("CACHE_DIR") + "/user_photo")
