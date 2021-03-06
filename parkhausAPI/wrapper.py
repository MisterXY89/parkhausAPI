
import requests
from .parkhaus import Parkhaus
from bs4 import BeautifulSoup, SoupStrainer
from .requestAssistant import RequestHeaderGenerator


class ParkhausWrapper:
    """
    ParkhausWrapper
    get html for specific car park in constance and parse data
    from it:
        - general data (content)
        - info about the places/spots in the car park (spots)
    Every car park has a name and a code, the code is the id required
    in order to build the specfic url for the car park.
    Furthermore an image will be parsed, if available

    Attributes
    ----------
    __baseUrl : str
        baseurl every car park url has
    __rhg : RequestHeaderGenerator
        object from helper class: generates random request headers
        -> helps to get blocked less
        see requestAssistant for more
    __places : dict
        all placenames as key with their corresponding code/int/id as value
    __codes : list
        all codes seperatly for easier code verification

    """

    def __init__(self):
        """
        Initialize all attributes, nothing special.
        The names and codes were looked up manually.
        """
        self.__baseUrl = "https://www.konstanz.de/site/Konstanz/node/"
        self.__rhg = RequestHeaderGenerator()
        self.__places = {
            "Altstadt": 107845,
            "Lago" : 107856,
            "Marktstätte" : 107867,
            "Fischmarkt" : 107878,
            "Döbele" : 107889,
            "Augustiner" : 107900,
            "Karstadt": 107900,
            "Benediktinerplatz" : 107911,
            "Seerhein-Center" : 107922,
            "Bodenseeforum" : 107933
        }
        self.__codes = [self.__places[key] for key in self.__places.keys()]
        self.__baseContentSelector = "basecontent-line-break-text"
        self.__spotsTableSelector = "plstabelle"


    def _buildUrlByName(self, name):
        """
        build car park url by name

        Parameters
        ----------
        name : str
            name of a car park

        Return
        ----------
        str, url for car park
        """
        if not name in self.__places:
            return "Name unknown / does not exist, run .getPlaces() for all codes and car park names."
        return self.__baseUrl + str(self.__places[name]) + "/Parkplatz.html"


    def _buildUrlByCode(self, code):
        """
        build car park url by name

        Parameters
        ----------
        name : int
            code of a car park

        Return
        ----------
        str, url for car park
        """
        if not code in self.__codes:
            return "Code does not exist, run .getPlaces() for all codes and car park names."
        return self.__baseUrl + code + "/Parkplatz.html"

    def getPlaces(self):
        """
        Get all car park names and their corresponding codes/ids/int

        Return
        ----------
        dict, places
        """
        return self.__places

    def _getSoup(self, code):
        """
        Reads site for given code (or name) and makes soup via bs4

        Parameters
        ----------
        code : int
            code of a car park
        | maybe:
        code : string
            name of car park

        Return
        ----------
        BeautifulSoup object,
        str/int status
        | maybe (if error):
        None,
        str, int, status
        """
        if type(code) != int:
            url = self._buildUrlByName(code)
        else:
            url = self._buildUrlByCode(code)
        if not "https" in url:
            return None, "UrlBuilding Error"
        try:
            response = requests.get(url, headers = self.__rhg.getRandomRequestHeader())
        except Exception as err:
            print(f"Error: {err}")
            return None, err
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "lxml")
            # print(f"OK! Url: {url}")
            return soup, 200
        else:
            print(f'Something went wrong. Got the following response code: {response.status_code}')
            return None, response.status_code


    def _parse(self, soup, spots=True, content=True):
        """
        main parse method, calls the specfic ones (spots, content, image)
        and merges results

        Parameters
        ----------
        soup : BeautifulSoup
            soup of car park html
        | maybe:
        spots : bool
            parse spots?
        | maybe:
        content : bool
            parse content?

        Return
        ----------
        dict, containing spots and content (image is part of content)
        """
        # TODO:
        # IndexError: list index out of range (-> not found)
        baseContent = soup.findAll("p", class_ = self.__baseContentSelector)[::-1][1]
        spotsTable = soup.findAll("table", class_ = self.__spotsTableSelector)[0]
        imageUrl = self._parseImage(soup)

        content = self._parseContent(baseContent)
        content["image"] = imageUrl
        spots = self._parseSpots(spotsTable)
        return {
            "content": content,
            "spots": spots
        }


    def _parseImage(self, soup):
        """
        parses the soup for image matching the car park

        Parameters
        ----------
        soup : BeautifulSoup
            soup of car park html

        Return
        ----------
        str, absolute url of image
        str, empty if none found
        """
        imageBaseUrl = "https://www.konstanz.de"
        imageUrl = ""
        imgs = soup.findAll("img")
        for img in imgs:
            if "alt" in img.attrs:
                alt = img["alt"].lower()
                if "parkhaus" in alt or "einfahrt" in alt:
                    imageUrl = imageBaseUrl + img["src"]
            else:
                continue

        return imageUrl


    def _parseSpots(self, spotsDiv):
        """
        parses the soup for the spots in the car park

        Parameters
        ----------
        spotsDiv : BeautifulSoup
            soup div containing spots info

        Return
        ----------
        dict, containing info about total, free, occupied spots
            and the free spots tendency (development)
        """
        rows = spotsDiv.findAll('tr')[1:]
        spots = int(rows[0].findAll("td")[0].text)
        free = int(rows[1].findAll("td")[0].text)
        occupied = int(rows[2].findAll("td")[0].text)
        tendency = rows[4].findAll("td")[0].findAll("span")[0]["titel"]
        return {
            "total": spots,
            "free": free,
            "occupied": occupied,
            "tendency": tendency
        }

    def _createObject(self, res):
        """
        creates Parkhaus object with given result from previous parsing

        Parameters
        ----------
        res : dict
            result from previous parsing the soup

        Return
        ----------
        Parkhaus
        """
        # entry, openingHours, hightLimit, address, operator, spots, freeSpots, occupiedSpots, tendency, image
        sp = res["spots"]
        cn = res["content"]#
        parkhaus = Parkhaus(cn["entry"], cn["openingHours"], cn["hightLimit"], cn["address"], cn["operator"], sp["total"], sp["free"], sp["occupied"], sp["tendency"], cn["image"])
        return parkhaus


    def _parseContent(self, contentDiv):
        """
        parses the soup for some meta info about the car park (contents)

        Parameters
        ----------
        contentDiv : BeautifulSoup
            soup div containing meta info (content)

        Return
        ----------
        dict, containing meta info
        """
        adjust = 0
        breakSplit = str(contentDiv).split("<br/>")
        entry = breakSplit[1]
        spanList = contentDiv.findAll("span")
        if(len(spanList) == 0):
            openingHours = breakSplit[4]
        else:
            openingHours = contentDiv.findAll("span")# [1].text
        hightLimit = breakSplit[5]
        if not "m" in hightLimit and not "," in hightLimit or "Ausfahrt" in hightLimit:
            hightLimit = breakSplit[8]
            adjust = 2
        address = breakSplit[(8+adjust):(11+adjust)]
        for el in address:
            if "Betreiber" in el:
                address = ""
                adjust = -2
        operator = breakSplit[(14+adjust):(18+adjust)]
        return {
            "entry": entry,
            "openingHours": openingHours,
            "hightLimit": hightLimit,
            "address": address,
            "operator": operator
        }

    def getInfo(self, name, spots=True, content=True):
        """
        public method starts the process of getting the soup, parsing it
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
        soup, status = self._getSoup(name)
        if status != 200:
            return status
        res = self._parse(soup, spots=spots, content=content)
        obj = self._createObject(res)
        return obj
