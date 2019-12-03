# pylint: disable=bare-except
"""Package to fetch livestream video links from CGTN"""
from enum import Enum
import time
import requests

from .config import REQUEST_TIMEOUT

class LivestreamChannel(Enum):
    """Class enum to represent CTGN livestream channels """

    ENGLISH = {'name': 'English Channel', 'prefix': 'english', 'suffix': 'news', 'id': '1'}
    SPANISH = {'name': 'Spanish Channel', 'prefix': 'espanol', 'suffix': 'e', 'id': '2'}
    FRENCH = {'name': 'French Channel', 'prefix': 'french', 'suffix': 'f', 'id': '3'}
    ARABIC = {'name': 'Arabic Channel', 'prefix': 'arabic', 'suffix': 'a', 'id': '4'}
    RUSSIAN = {'name': 'Russian Channel', 'prefix': 'russian', 'suffix': 'r', 'id': '5'}
    DOCUMENTARY = {'name': 'Documentary Channel', 'prefix': 'document', 'suffix': 'doc', 'id': '6'}

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

    LIVE_BASE_URL = "https://news.cgtn.com/resource/live/{0}/cgtn-{1}.m3u8"
    SCHED_BASE_URL = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId={0}"
    VIDEO_BASE_URL = "https://api.cgtn.com/website/api/live/channel/epg/playback?channelId={0}&epgId={1}"

    @staticmethod
    def parse_current_live(channel):
        """Funtion to fetch livestream data per region """

        if channel not in LivestreamChannel:
            return None

        now = int(round(time.time() * 1000))
        now_min_2h = now - (2 * 60 * 60 * 1000)

        live_url = LivestreamParser.LIVE_BASE_URL.format(channel.value["prefix"], channel.value["suffix"])
        schedule_url = LivestreamParser.SCHED_BASE_URL.format(channel.value["id"])

        try:
            search_url = '{}&startTime={}&endTime={}'.format(schedule_url, now_min_2h, now)
            print(search_url)
            req = requests.get(search_url, timeout=REQUEST_TIMEOUT)
            req.raise_for_status()
            json = req.json()
            if json['status'] == 200 and json['data']:
                for item in json['data']:
                    if int(item['startTime']) < now < int(item['endTime']):
                        program = item['name']
                        start = item['startTime']
                        end = item['endTime']
                        return Livestream(video_url=live_url, program=program, start=start, end=end)
        except:
            pass

        return None
