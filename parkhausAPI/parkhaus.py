

class Parkhaus:
    """
    Class used to represent information about a car park

    Attributes
    ----------
    entry : str
        how and/or where to enter the car park
    entry : str
        how and/or where to enter the car park
    openingHours : str
        opening hours of the car park
    hightLimit : str
        empty if none / is a string in the format: x,yz m with x,y,z number
    address : str
        street, housenr and postal code
    operator : str
        address and name of the car house operator
    spots : int
        total number of available spots
    freeSpots : int
        free spots
    occupiedSpots : int
        occupied spots
    tendency : str
        tendency of free spots development: gleichbleibend, steigend or sinkend
    image : str
        an absolute image url of (the entry of) the car park
    """

    def __init__(self, entry, openingHours, hightLimit, address, operator, spots, freeSpots, occupiedSpots, tendency, image):
        self.entry = entry
        self.openingHours = openingHours
        self.hightLimit = hightLimit
        self.address = address
        self.operator = operator
        self.spots = spots
        self.freeSpots = freeSpots
        self.occupiedSpots = occupiedSpots
        self.tendency = tendency
        self.image = image
