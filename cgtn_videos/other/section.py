# -*- coding: utf-8 -*-
# pylint: disable=bare-except
"""Package to represent CGTN sections for regions other then EN """
from enum import Enum
import concurrent.futures
import requests

from ..config import REQUEST_TIMEOUT
from ..video import Video

class SectionFR(Enum):
    """Class enum to represent CTGN sections for French region """

    ALL = {'id': '', 'name': 'Tous', 'name_en': 'All'}
    CHINE = {'id': '1', 'name': 'Chine', 'name_en': 'China'}
    MONDE = {'id': '2', 'name': 'Monde', 'name_en': 'World'}
    ECONOMIE = {'id': '3', 'name': 'Économie', 'name_en': 'Economy'}
    OPINIONS = {'id': '4', 'name': 'Opinions', 'name_en': 'Opinions'}
    CULTURE = {'id': '5', 'name': 'Culture', 'name_en': 'Culture'}
    SPORT = {'id': '6', 'name': 'Sport', 'name_en': 'Sport'}
    MONDE_2 = {'id': '7', 'name': 'Monde', 'name_en': 'World'}
    AFRIQUE = {'id': '8', 'name': 'Afrique', 'name_en': 'Africa'}
    MONDE_3 = {'id': '9', 'name': 'Monde', 'name_en': 'World'}
    EXCLUSIVITES = {'id': '10', 'name': 'Exclusivités', 'name_en': 'Exclusives'}
    VIDEOS = {'id': '11', 'name': 'Vidéos', 'name_en': 'Videos'}

class SectionAR(Enum):
    """Class enum to represent CTGN sections for Arab region """

    ALL = {'id': '', 'name': 'الكل', 'name_en': 'All'}
    CHINA = {'id': '1', 'name': 'الصين', 'name_en': 'China'}
    INTERNATIONAL = {'id': '2', 'name': 'دولي', 'name_en': 'International'}
    ARABIC = {'id': '3', 'name': 'عربي', 'name_en': 'Arabic'}
    DIALOGUE_AND_COMMENTS = {'id': '4', 'name': 'الحوار والتعليقات', 'name_en': 'Dialogue and Comments'}

class SectionSP(Enum):
    """Class enum to represent CTGN sections for Spanish region """

    ALL = {'id': '', 'name': 'Todo', 'name_en': 'All'}
    CHINA = {'id': '1', 'name': 'China', 'name_en': 'China'}
    MUNDO = {'id': '2', 'name': 'Mundo', 'name_en': 'World'}
    IBERO_AMERICA = {'id': '3', 'name': 'Iberoamérica', 'name_en': 'Latin America'}
    ECONOMIA = {'id': '4', 'name': 'Economía', 'name_en': 'Economy'}
    CULTURA = {'id': '5', 'name': 'Cultura', 'name_en': 'Culture'}
    DEPORTES = {'id': '6', 'name': 'Deportes', 'name_en': 'Sports'}
    OTHER = {'id': '7', 'name': 'Other', 'name_en': 'Other'}

class SectionRU(Enum):
    """Class enum to represent CTGN sections for Russian region """

    ALL = {'id': '', 'name': 'все', 'name_en': 'All'}
    POLITICS_ECONOMICS = {'id': '1', 'name': 'Политика/Экономика', 'name_en': 'Politics / Economics'}
    SCIENCE_EDUCATION = {'id': '2', 'name': 'Наука/Образование', 'name_en': 'Science / Education'}
    CULTURE_SPORT = {'id': '3', 'name': 'Культура/Спорт', 'name_en': 'Culture / Sports'}
    SOCIETY = {'id': '4', 'name': 'Общество', 'name_en': 'Society'}
    CHINA = {'id': '5', 'name': 'Китай', 'name_en': 'China'}
    EURASIA = {'id': '6', 'name': 'Евразия', 'name_en': 'Eurasia'}
    WORLD = {'id': '7', 'name': 'мир', 'name_en': 'World'}


class SectionParser(object):
    """Class to parse CGTN section videos for regions other then EN """
    BASE_URL = "https://language-api.cgtn.com/api/news/sectionNews"

    @staticmethod
    def parse_section_fr(section_id):
        """Funtion to fetch section videos for the FR region """
        return SectionParser.__parse(SectionParser.BASE_URL + "?channel=1&pageSize=100&sectionId={}".format(section_id))

    @staticmethod
    def parse_section_ar(section_id):
        """Funtion to fetch section videos for the AR region """
        return SectionParser.__parse(SectionParser.BASE_URL + "?channel=2&pageSize=100&sectionId={}".format(section_id))

    @staticmethod
    def parse_section_sp(section_id):
        """Funtion to fetch section videos for the SP region """
        return SectionParser.__parse(SectionParser.BASE_URL + "?channel=3&pageSize=100&sectionId={}".format(section_id))

    @staticmethod
    def parse_section_ru(section_id):
        """Funtion to fetch section videos for the RU region """
        return SectionParser.__parse(SectionParser.BASE_URL + "?channel=4&pageSize=100&sectionId={}".format(section_id))

    @staticmethod
    def __parse(url):
        """Funtion to fetch section videos for regions other then EN """
        videos = set()
        total_count = SectionParser.__parse_total_count(url)
        max_workers = total_count / 100 + 1

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_video_m3u8 = {
                executor.submit(SectionParser.__parse_page, url, i): i
                for i in range(0, total_count, 100)
                }
            for future in concurrent.futures.as_completed(future_to_video_m3u8):
                videos.update(future.result())

        return list(videos)

    @staticmethod
    def __parse_total_count(url):
        """Funtion to fetch section video total count for regions other then EN """
        url += "&start={}".format("0")
        try:
            request = requests.get(url, timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
            json = request.json()
            if json['status'] == 200 and json['data']:
                return json['total']
        except:
            pass
        return 0

    @staticmethod
    def __parse_page(url, start):
        """Funtion to fetch section videos for regions other then EN """
        videos = []
        url += "&start={}".format(start)
        print(url)

        try:
            request = requests.get(url, timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
            json = request.json()
            if json['status'] == 200 and json['data']:
                for json_video in json['data']:
                    try:
                        if not 'coverVideo' in json_video:
                            continue
                        video = SectionParser.__parse_video(json_video)
                        videos.append(video)
                    except:
                        continue
        except:
            pass

        return videos

    @staticmethod
    def __parse_video(json):
        """Helper function to parse json into video object """
        uid = json['id']
        video_url = json['coverVideo']
        img_url = json['coverUrl']
        web_url = json['link']
        title = json['headline']
        details = None
        if 'abstracts' in json:
            details = json['abstracts']
        editor = json['editorName']
        publish_date = json['publishDate']

        return Video(uid=uid, video_url=video_url, img_url=img_url, web_url=web_url,
                     title=title, details=details, editor=editor, publish_date=publish_date)
