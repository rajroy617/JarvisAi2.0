import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import eel
from Backend.feature import *
from Backend.command import *



import eel
from Backend.feature import *
from Backend.command import *

eel.init("Frontend")

play_assistant_sound()

def start():
    eel.start(
        "index.html",
        mode="edge",
        host="127.0.0.1",
        port=8000,
        block=True
)