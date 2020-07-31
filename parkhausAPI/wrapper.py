
import requests
from .parkhaus import Parkhaus
from bs4 import BeautifulSoup, SoupStrainer
from .requestAssistant import RequestHeaderGenerator


class ParkhausWrapper:
    """
    docstring for ParkhausWrapper.
    """

    def __init__(self):
        # self.baseUrl = "https://www.konstanz.de/,Lde/start/leben+in+konstanz/parkleitsystem.html"
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
        self.baseContentSelector = "basecontent-line-break-text"
        self.spotsTableSelector = "plstabelle"

    def _buildUrlByName(self, name):
        return self.__baseUrl + str(self.__places[name]) + "/Parkplatz.html"

    def _buildUrlByCode(self, code):
        return self.__baseUrl + code + "/Parkplatz.html"

    def getPlaces(self):
        return self.__places

    def _getSoup(self, code):
        if type(code) != int:
            url = self._buildUrlByName(code)
        else:
            url = self._buildUrlByCode(code)
        try:
            response = requests.get(url, headers = self.__rhg.getRandomRequestHeader())
        except Exception as err:
            print(f"Error: {err}")
            return None, err
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "lxml")
            print(f"OK! Url: {url}")
            return soup, 200
        else:
            print(f'Something went wrong. Got the following response code: {response.status_code}')
            return None, response.status_code

    def _parse(self, soup):
        baseContent = soup.findAll("p", class_ = self.baseContentSelector)[::-1][1]
        spotsTable = soup.findAll("table", class_ = self.spotsTableSelector)[0]
        imageUrl = self._parseImage(soup)

        content = self._parseContent(baseContent)
        content["image"] = imageUrl
        spots = self._parseSpots(spotsTable)
        return {
            "content": content,
            "spots": spots
        }


    def _parseImage(self, soup):
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
        # entry, openingHours, hightLimit, address, operator, spots, freeSpots, occupiedSpots, tendency, image
        sp = res["spots"]
        cn = res["content"]#
        parkhaus = Parkhaus(cn["entry"], cn["openingHours"], cn["hightLimit"], cn["address"], cn["operator"], sp["total"], sp["free"], sp["occupied"], sp["tendency"], cn["image"])
        return parkhaus


    def _parseContent(self, contentDiv):
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

    def main(self):
        soup, status = self._getSoup("Döbele")
        if status != 200:
            return status
        res = self._parse(soup)
        obj = self._createObject(res)
        attrs = vars(obj)
        for key in attrs:
            print("%s : %s" %(key, attrs[key]))
