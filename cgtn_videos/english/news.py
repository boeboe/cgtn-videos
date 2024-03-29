# pylint: disable=bare-except
"""Package to fetch videos from CGTN """
import re
import concurrent.futures
import requests
import html5lib

from bs4 import BeautifulSoup
from ..config import REQUEST_TIMEOUT
from ..video import Video

class NewsParser(object):
    """Class to parse news videos from CGTN """

    @staticmethod
    def parse_video_count(url):
        """Funtion to fetch the amount of news videos per category from CGTN EN """
        amount = 0
        try:
            request = requests.get(url, timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
            soup = BeautifulSoup(request.content, "html5lib")
            amount = len(soup.find_all("div", {"class": "cg-video"}))
        except:
            return amount
        return amount

    @staticmethod
    def parse_videos(url, paged=False, offset=0, page_size=0):
        """Funtion to fetch news videos per category from CGTN EN """
        videos = []
        try:
            request = requests.get(url, timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
            soup = BeautifulSoup(request.content, "html5lib")
            video_item_list = soup.find_all("div", {"class": "cg-video"})

            if not paged:
                for video_item in video_item_list:
                    video = NewsParser.__parse_video(video_item)
                    if video:
                        videos.append(video)
            elif paged and offset * page_size < len(video_item_list):
                for i in range(offset * page_size, offset * page_size + page_size):
                    try:
                        video_item = video_item_list[i]
                        video = NewsParser.__parse_video(video_item)
                        if video:
                            videos.append(video)
                    except IndexError:
                        break
            if videos:
                videos = NewsParser.__process_m3u8_links(videos)
        except:
            pass

        return videos

    @staticmethod
    def __parse_video(html):
        """Parse a single video item """
        if not html.a["data-label"]:
            return None
        uid = html.a["data-news-id"]
        title = html.a["data-label"]
        img_url = html.find_all("a")[-1].div.img["data-original"]
        video_url = img_url.replace(".jpg", ".m3u8").replace(".jpeg", ".m3u8").replace(".png", ".m3u8")
        web_url = html.a["href"]
        if not web_url.startswith("http"):
            web_url = "https://www.cgtn.com" + web_url
        publish_date = html.a["data-time"]
        video = Video(uid=uid, video_url=video_url, img_url=img_url, web_url=web_url,
                      title=title, publish_date=publish_date)
        return video

    @staticmethod
    def __check_m3u8_link(video):
        """Check if m3u8 link is valid and fix if not by making an extra call to the news page """
        try:
            request = requests.get(video.web_url, timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
            if not "#EXTM3U" in request.text:
                try:
                    fallback_request = requests.get(video.web_url, timeout=REQUEST_TIMEOUT)
                    fallback_request.raise_for_status()
                except:
                    pass
                fallback_soup = BeautifulSoup(fallback_request.content, "html5lib")
                fallback_items = fallback_soup.find_all('div', {'data-video': re.compile(r'.m3u8')})
                video.video_url = fallback_items[0]["data-video"]
        except:
            pass
        return video

    @staticmethod
    def __process_m3u8_links(videos):
        """Helper methods to check if m3u8 links are valid and fix if not the case """
        result_videos = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(videos)) as executor:
            future_to_video_m3u8 = {
                executor.submit(NewsParser.__check_m3u8_link, video): video
                for video in videos
                }
            for future in concurrent.futures.as_completed(future_to_video_m3u8):
                result_videos.append(future.result())
        return result_videos
