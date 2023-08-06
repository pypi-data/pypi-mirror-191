"""Simple_Pygame is a set of Python modules that provides many features using pygame and other packages. It can help you create multimedia applications much easier and save you a lot of time."""
from .version import __version__

def init() -> None:
    "Initialize all Simple_Pygame modules."
    global mixer
    from . import mixer