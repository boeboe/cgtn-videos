# pylint: disable=bare-except
"""Package to fetch special videos from CGTN """
import requests
import html5lib

from bs4 import BeautifulSoup
from ..config import REQUEST_TIMEOUT

class NewsSpecial(object):
    """Class to represent videos from CGTN """

    def __init__(self, key=None, name=None, url=None, img_url=None):
        self.key = key
        self.name = name
        self.url = url
        self.img_url = img_url

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class NewsSpecialParser(object):
    """Class to parse special categories from CGTN EN """
    BASE_URL = "https://www.cgtn.com/special-list/{}.html"

    @staticmethod
    def parse_specials(year):
        """Funtion to fetch special news categories from CGTN EN """
        specials = []

        try:
            request = requests.get(NewsSpecialParser.BASE_URL.format(year), timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
            soup = BeautifulSoup(request.content, "html5lib")
            special_item_list = soup.find_all("div", {"class": ["cg-newsWrapper", "cg-padding-tb"]})

            for special_item in special_item_list:
                key = special_item.div.a['data-news-id']
                name = special_item.div.a['data-label']
                url = special_item.div.a['href']
                img_url = special_item.div.a.img['data-original']
                specials.append(NewsSpecial(key=key, name=name, url=url, img_url=img_url))
        except:
            pass

        return specials
