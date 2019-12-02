# pylint: disable=bare-except
"""Package to fetch livestream video links from CGTN"""
import time
import requests

from .region import Region
from .config import REQUEST_TIMEOUT

class Livestream(object):
    """Class to represent CGTN Livestreams """

    def __init__(self, video_url=None, program=None, start=None, end=None):
        self.video_url = video_url
        self.program = program
        self.start = start
        self.end = end

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class LivestreamParser(object):
    """Class to parse CGTN Livestreams """

    @staticmethod
    def parse(region):
        """Funtion to fetch livestream data per region """

        now = int(round(time.time() * 1000))
        now_min_2h = now - (2 * 60 * 60 * 1000)
        now_add_2h = now + (2 * 60 * 60 * 1000)

        if region == Region.ENGLISH:
            video_url = "https://news.cgtn.com/resource/live/english/cgtn-news.m3u8"
            schedule_url = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId=1"
        elif region == Region.SPANISH:
            video_url = "https://news.cgtn.com/resource/live/espanol/cgtn-e.m3u8"
            schedule_url = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId=2"
        elif region == Region.FRENCH:
            video_url = "https://news.cgtn.com/resource/live/french/cgtn-f.m3u8"
            schedule_url = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId=3"
        elif region == Region.ARABIC:
            video_url = "https://news.cgtn.com/resource/live/arabic/cgtn-a.m3u8"
            schedule_url = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId=4"
        elif region == Region.RUSSIAN:
            video_url = "https://news.cgtn.com/resource/live/russian/cgtn-r.m3u8"
            schedule_url = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId=5"
        elif region == Region.DOCUMENTARY:
            video_url = "https://news.cgtn.com/resource/live/document/cgtn-doc.m3u8"
            schedule_url = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId=6"
        else:
            return None

        try:
            req = requests.get('{}&startTime={}&endTime={}'.format(schedule_url, now_min_2h, now_add_2h), timeout=REQUEST_TIMEOUT)
            req.raise_for_status()
        except:
            return None

        json = req.json()
        if json['status'] == 200 and json['data']:
            for item in json['data']:
                if int(item['startTime']) < now < int(item['endTime']):
                    program = item['name']
                    start = item['startTime']
                    end = item['endTime']
                    break

        return Livestream(video_url=video_url, program=program, start=start, end=end)
