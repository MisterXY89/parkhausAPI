
from .wrapper import *

class API:
    """
    Interface for the ParkhausWrapper

    Attributes
    ----------
    wrapper : ParkhausWrapper
        used to perform the tasks
        -> see wrapper.py for detailed doc
    """

    def __init__(self):
        self.wrapper = ParkhausWrapper()

    def getInfo(self, name, spots=True, content=True):
        """
        calls getInfo on wrapper:
        starts the process of getting the soup, parsing it
        and creating the parkhaus object

        Parameters
        ----------
        name : str
            name of the car park
        | maybe:
        name : int
            code of the car park
        | maybe:
        spots : bool
            parse spots?
        | maybe:
        content : bool
            parse content?

        Return
        ----------
        parkhaus object with all infos
        """
        if not spots and content or spots and not content:
            obj = self.wrapper.getInfo(name, spots=spots, content=content)
        else:
            obj = self.wrapper.getInfo(name)
        return obj

    def getPlaces(self):
        """
        Get all car park names and their corresponding codes/ids/int

        Return
        ----------
        dict, places
        """
        return self.wrapper.getPlaces()
