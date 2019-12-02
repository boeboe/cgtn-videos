# pylint: disable=bare-except
"""Package to fetch program video links from CGTN EN """
import requests

from .config import REQUEST_TIMEOUT

class ProgramVideo(object):
    """Class to represent CGTN EN program videos """

    def __init__(self, **kwargs):
        self.video_url = kwargs.get("video_url")
        self.poster_url = kwargs.get("poster_url")
        self.detail_url = kwargs.get("detail_url")
        self.share_url = kwargs.get("share_url")
        self.headline = kwargs.get("headline")
        self.publish_time = kwargs.get("publish_time")
        self.editor = kwargs.get("editor")

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

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
                        video_url = video['coverVideo'][0]['video']['url']
                        poster_url = video['coverVideo'][0]['poster']['url']
                        detail_url = video['detailUrl']
                        share_url = video['shareUrl']
                        headline = video['shortHeadline']
                        publish_time = video['publishTime']
                        editor = video['editorName']

                        videos.append(ProgramVideo(video_url=video_url,
                                                   poster_url=poster_url,
                                                   detail_url=detail_url,
                                                   share_url=share_url,
                                                   headline=headline,
                                                   publish_time=publish_time,
                                                   editor=editor))
                    except:
                        continue
        except:
            pass

        return videos
