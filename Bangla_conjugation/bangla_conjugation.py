import random, time
from enum import IntEnum

from pyscript.web import page, when

def make_ready():
    """
    When the page loads, hide the loading text and show the content
    """
    loadingbox = page["#loadingbox"]
    loadingbox.classes.add("loaded")

    vertical = page["#vertical"]
    vertical.classes.remove("loading")

# ON PAGE LOAD
make_ready() # hide loading, show content