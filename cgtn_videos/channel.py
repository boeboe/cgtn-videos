# pylint: disable=bare-except
"""Package to fetch channel video links from CGTN"""
from enum import Enum
import calendar
import concurrent.futures
import datetime
import time
import requests

from .config import REQUEST_TIMEOUT
from .video import Video

class Channel(Enum):
    """Class enum to represent CTGN channels """

    ENGLISH = {'name': 'English Channel', 'prefix': 'english', 'suffix': 'news', 'id': '1'}
    SPANISH = {'name': 'Spanish Channel', 'prefix': 'espanol', 'suffix': 'e', 'id': '2'}
    FRENCH = {'name': 'French Channel', 'prefix': 'french', 'suffix': 'f', 'id': '3'}
    ARABIC = {'name': 'Arabic Channel', 'prefix': 'arabic', 'suffix': 'a', 'id': '4'}
    RUSSIAN = {'name': 'Russian Channel', 'prefix': 'russian', 'suffix': 'r', 'id': '5'}
    DOCUMENTARY = {'name': 'Documentary Channel', 'prefix': 'document', 'suffix': 'doc', 'id': '6'}

class ChannelParser(object):
    """Class to parse CGTN channel videos """

    LIVE_BASE_URL = "https://news.cgtn.com/resource/live/{0}/cgtn-{1}.m3u8"
    SCHED_BASE_URL = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId={0}&startTime={1}&endTime={2}"
    DATA_BASE_URL = "https://api.cgtn.com/website/api/live/channel/epg/playback?channelId={0}&epgId={1}" + \
                    "&startTime={2}&endTime={3}"

    @staticmethod
    def parse_current_live(channel):
        """Method to fetch channel livestream video per region """

        if channel not in Channel:
            return None

        now = int(round(time.time() * 1000))
        now_min_2h = now - (2 * 60 * 60 * 1000)
        live_url = ChannelParser.LIVE_BASE_URL.format(channel.value["prefix"], channel.value["suffix"])
        schedule_url = ChannelParser.SCHED_BASE_URL.format(channel.value["id"], now_min_2h, now)

        try:
            req = requests.get(schedule_url, timeout=REQUEST_TIMEOUT)
            req.raise_for_status()
            json = req.json()
            if json['status'] == 200 and json['data']:
                for item in json['data']:
                    if int(item['startTime']) < now < int(item['endTime']):
                        video = ChannelParser.__parse_video(item)
                        video.video_url = live_url
                        return video
        except:
            pass
        return None

    @staticmethod
    def parse_history_count(channel):
        """Method to fetch channel history videos count per region """

        if channel not in Channel:
            return None

        now = int(round(time.time() * 1000))
        schedule_url = ChannelParser.SCHED_BASE_URL.format(channel.value["id"], 0, now)
        try:
            req = requests.get(schedule_url, timeout=REQUEST_TIMEOUT * 4)
            req.raise_for_status()
            return req.text.count("channelId") - 1
        except:
            pass
        return 0

    @staticmethod
    def parse_history_by_month(channel, day=None, month=None, year=None):
        """Method to fetch channel history videos for a month or day """
        (begin, end) = ChannelParser.__get_window_epoch(year=year, month=month, day=day)
        return ChannelParser.parse_history_by_window(channel, begin=begin, end=end)

    @staticmethod
    def parse_history_from_now(channel, hours=None):
        """Method to fetch channel history videos within on a number of hours from now """
        now = int(round(time.time() * 1000))
        begin = now - hours * 60 * 60 * 1000
        return ChannelParser.parse_history_by_window(channel, begin=begin, end=now)

    @staticmethod
    def parse_history_by_window(channel, begin=None, end=None):
        """Method to fetch channel history videos for a certain window defined by begin and end """
        videos_no_m3u8 = []
        videos = []

        if channel not in Channel:
            return []

        schedule_url = ChannelParser.SCHED_BASE_URL.format(channel.value["id"], begin, end)
        try:
            req = requests.get(schedule_url, timeout=REQUEST_TIMEOUT * 4)
            req.raise_for_status()
            json = req.json()
            if json['status'] == 200 and json['data']:
                for item in json['data'][1:]:
                    videos_no_m3u8.append(ChannelParser.__parse_video(item))

                with concurrent.futures.ThreadPoolExecutor(max_workers=len(videos_no_m3u8)) as executor:
                    future_to_video_m3u8 = {
                        executor.submit(ChannelParser.__parse_video_m3u8, channel, video): video
                        for video in videos_no_m3u8
                        }
                    for future in concurrent.futures.as_completed(future_to_video_m3u8):
                        videos.append(future.result())
        except:
            pass
        return videos

    @staticmethod
    def __parse_video_m3u8(channel, video):
        """Helper method to fetch the m3u8 video stream link """
        data_url = ChannelParser.DATA_BASE_URL.format(channel.value["id"], video.uid, video.start_date, video.end_date)

        try:
            req = requests.get(data_url, timeout=REQUEST_TIMEOUT * 2)
            req.raise_for_status()
            json = req.json()
            if json['status'] == 200 and json['data']:
                video.video_url = json['data']
        except:
            pass
        return video

    @staticmethod
    def __get_window_epoch(day=None, month=None, year=None):
        """Helper method to retrieve the first and last millisecond of a day/month/year combination """
        if day:
            first = datetime.datetime(year, month, day, 0, 0, 0, 0)
            last = datetime.datetime(year, month, day, 23, 59, 59, 999999)
        else:
            days_in_month = calendar.monthrange(year, month)[1]
            first = datetime.datetime(year, month, 1, 0, 0, 0, 0)
            last = datetime.datetime(year, month, days_in_month, 23, 59, 59, 999999)
        return (int(first.strftime('%s'))*1000, int(last.strftime('%s'))*1000)

    @staticmethod
    def __parse_video(json):
        """Helper method to parse the channel video metadata """
        uid = json['epgId']
        name = json['name']
        start = json['startTime']
        end = json['endTime']
        return Video(uid=uid, video_url=None, title=name, start_date=start, end_date=end)
