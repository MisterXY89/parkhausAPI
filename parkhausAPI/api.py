
from .wrapper import *

class API:
    """docstring for API."""

    def __init__(self):
        self.wrapper = ParkhausWrapper()

    def getInfo(self, name, spots=True, content=True):
        if not spots and content or spots and not content:
            obj = self.wrapper.getInfo(name, spots=spots, content=content)
        else:
            obj = self.wrapper.getInfo(name)
        return obj

    def getPlaces(self):
        return self.wrapper.getPlaces()
