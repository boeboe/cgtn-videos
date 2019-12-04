# pylint: disable=bare-except
"""Package to fetch program video links from CGTN EN """
import requests

from ..config import REQUEST_TIMEOUT
from ..video import Video

class ProgramParser(object):
    """Class to parse CGTN EN Program Videos """

    @staticmethod
    def parse_programs():
        """Funtion to fetch program videos for the EN region """
        return ProgramParser.__parse("https://api.cgtn.com/website/api/program/getList")

    @staticmethod
    def parse_topnews():
        """Funtion to fetch topnews videos for the EN region """
        return ProgramParser.__parse("https://api.cgtn.com/website/api/news/topnews")

    @staticmethod
    def __parse(url):
        """Funtion to fetch program videos for the EN region """
        videos = []

        try:
            request = requests.get(url, timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
            json = request.json()
            if json['status'] == 200 and json['data']:
                for video in json['data']:
                    try:
                        video = ProgramParser.__parse_video(json)
                        videos.append(video)
                    except:
                        continue
        except:
            pass

        return videos

    @staticmethod
    def __parse_video(json):
        """Parse a single video item """
        uid = json['newsId']
        video_url = json['coverVideo'][0]['video']['url']
        poster_url = json['coverVideo'][0]['poster']['url']
        web_url = json['shareUrl']
        title = json['shortHeadline']
        editor = json['editorName']
        details = json['summary']
        publish_date = json['publishTime']

        return Video(uid=uid, video_url=video_url, img_url=poster_url, web_url=web_url,
                     title=title, details=details, editor=editor, publish_date=publish_date)
