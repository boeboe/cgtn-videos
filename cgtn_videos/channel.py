# pylint: disable=bare-except
"""Package to fetch channel program video links from CGTN"""
from enum import Enum
import calendar
import concurrent.futures
import datetime
import time
import requests

from .config import REQUEST_TIMEOUT

class Channel(Enum):
    """Class enum to represent CTGN channels """

    ENGLISH = {'name': 'English Channel', 'prefix': 'english', 'suffix': 'news', 'id': '1'}
    SPANISH = {'name': 'Spanish Channel', 'prefix': 'espanol', 'suffix': 'e', 'id': '2'}
    FRENCH = {'name': 'French Channel', 'prefix': 'french', 'suffix': 'f', 'id': '3'}
    ARABIC = {'name': 'Arabic Channel', 'prefix': 'arabic', 'suffix': 'a', 'id': '4'}
    RUSSIAN = {'name': 'Russian Channel', 'prefix': 'russian', 'suffix': 'r', 'id': '5'}
    DOCUMENTARY = {'name': 'Documentary Channel', 'prefix': 'document', 'suffix': 'doc', 'id': '6'}

class ChannelProgram(object):
    """Class to represent CGTN channel programs """

    def __init__(self, **kwargs):
        self.epg_id = kwargs.get("epg_id")
        self.channel_id = kwargs.get("channel_id")
        self.video_url = kwargs.get("video_url")
        self.name = kwargs.get("name")
        self.start = kwargs.get("start")
        self.end = kwargs.get("end")

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class ChannelParser(object):
    """Class to parse CGTN channel programs """

    LIVE_BASE_URL = "https://news.cgtn.com/resource/live/{0}/cgtn-{1}.m3u8"
    SCHED_BASE_URL = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId={0}&startTime={1}&endTime={2}"
    DATA_BASE_URL = "https://api.cgtn.com/website/api/live/channel/epg/playback?channelId={0}&epgId={1}" + \
                    "&startTime={2}&endTime={3}"

    @staticmethod
    def parse_current_live(channel):
        """Method to fetch channel livestream per region """

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
                        program = ChannelParser.__parse_program(item)
                        program.video_url = live_url
                        return program
        except:
            pass
        return None

    @staticmethod
    def parse_history_count(channel):
        """Method to fetch channel history video count per region """

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
        """Method to fetch channel history video for a month or day per region """
        (begin, end) = ChannelParser.__get_window_epoch(year=year, month=month, day=day)
        return ChannelParser.parse_history_by_window(channel, begin=begin, end=end)

    @staticmethod
    def parse_history_from_now(channel, hours=None):
        """Method to fetch channel history video within on a number of hours from now """
        now = int(round(time.time() * 1000))
        begin = now - hours * 60 * 60 * 1000
        return ChannelParser.parse_history_by_window(channel, begin=begin, end=now)

    @staticmethod
    def parse_history_by_window(channel, begin=None, end=None):
        """Method to fetch channel history video for a certain window defined by begin and end """
        programs_no_m3u8 = []
        programs = []

        if channel not in Channel:
            return []

        schedule_url = ChannelParser.SCHED_BASE_URL.format(channel.value["id"], begin, end)
        try:
            req = requests.get(schedule_url, timeout=REQUEST_TIMEOUT * 4)
            req.raise_for_status()
            json = req.json()
            if json['status'] == 200 and json['data']:
                for item in json['data'][1:]:
                    programs_no_m3u8.append(ChannelParser.__parse_program(item))

                with concurrent.futures.ThreadPoolExecutor(max_workers=len(programs_no_m3u8)) as executor:
                    future_to_program_m3u8 = {
                        executor.submit(ChannelParser.__parse_program_m3u8, p): p
                        for p in programs_no_m3u8
                        }
                    for future in concurrent.futures.as_completed(future_to_program_m3u8):
                        programs.append(future.result())
        except:
            pass
        return programs

    @staticmethod
    def __parse_program_m3u8(program):
        """Helper method to fetch the m3u8 video stream link """
        data_url = ChannelParser.DATA_BASE_URL.format(program.channel_id, program.epg_id, program.start, program.end)

        try:
            req = requests.get(data_url, timeout=REQUEST_TIMEOUT * 2)
            req.raise_for_status()
            json = req.json()
            if json['status'] == 200 and json['data']:
                program.video_url = json['data']
        except:
            pass
        return program

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
    def __parse_program(json):
        """Helper method to parse the channel program metadata """
        epg_id = json['epgId']
        channel_id = json['channelId']
        name = json['name']
        start = json['startTime']
        end = json['endTime']
        return ChannelProgram(epg_id=epg_id, channel_id=channel_id, video_url=None,
                              name=name, start=start, end=end)
