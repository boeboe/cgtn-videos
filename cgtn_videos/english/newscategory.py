# pylint: disable=bare-except
"""Package to fetch news categories from CGTN EN """
import re
import requests
import html5lib

from bs4 import BeautifulSoup
from ..config import REQUEST_TIMEOUT

class NewsCategory(object):
    """Class to represent news categories from CGTN EN """

    def __init__(self, key=None, name=None, url=None):
        self.key = key
        self.name = name
        self.url = url
        self.has_subcatagories = False

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class NewsCategoryParser(object):
    """Class to parse news categories from CGTN EN """
    NO_SUBCAT_LIST = ["china", "sports", "tech-sci", "world", "culture", "transcripts", "opinions", "video"]
    BASE_URL = "https://www.cgtn.com"

    @staticmethod
    def parse_categories():
        """Funtion to fetch news categories from CGTN EN """
        categories = []
        ignore_categories = ["Specials", "Picture"]

        try:
            request = requests.get(NewsCategoryParser.BASE_URL, timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
            soup = BeautifulSoup(request.content, "html5lib")
            footer = soup.find("div", {"class": "cg-footer cg-max-footer"})

            for item in footer.find_all("a", {"data-action": "Sitemap_Click"}):
                if item.text.strip() in ignore_categories:
                    continue
                cat = NewsCategory(key=item['href'].split("/")[-1],
                                   name=item.text.strip().capitalize(),
                                   url=item['href'])
                if cat.key not in NewsCategoryParser.NO_SUBCAT_LIST:
                    cat.has_subcatagories = True
                categories.append(cat)
        except:
            pass

        return categories

    @staticmethod
    def parse_sub_categories(url):
        """Funtion to fetch news subcategories from CGTN EN """
        category = url.split("/")[-1]
        subcategories = []
        subcategories_keys = []

        if category in NewsCategoryParser.NO_SUBCAT_LIST:
            return subcategories

        try:
            request = requests.get(url, timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
            soup = BeautifulSoup(request.content, "html5lib")

            for item in soup.find_all('a', {'href': re.compile(r'/{}/'.format(category))}):
                key = item['href'].split("/")[-1].split(".")[0]

                if key in ["china", "log"] or key in subcategories_keys:
                    continue

                if NewsCategoryParser.BASE_URL not in item['href']:
                    url = NewsCategoryParser.BASE_URL + item['href']
                else:
                    url = item['href']

                if not item.text.strip():
                    name = key.replace("-", " ").capitalize()
                elif item.text.strip().capitalize() == "More":
                    name = key.capitalize()
                else:
                    name = item.text.strip().capitalize()

                subcat = NewsCategory(key=key, name=name, url=url)
                subcategories.append(subcat)
                subcategories_keys.append(key)
        except:
            pass

        return subcategories
