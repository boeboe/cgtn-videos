# pylint: disable=bare-except
"""Package to test Videos """
import unittest
import requests

from cgtn_videos.video import Video, VideoParser
from cgtn_videos.config import REQUEST_TIMEOUT

class VideoTest(unittest.TestCase):
    """Class to test Video """

    def test_constructor(self):
        '''Test function '''
        video = Video(data_id="A", title="B", video_url="C", img_url="D", web_url="E", date="F")

        self.assertEqual(video.data_id, "A")
        self.assertEqual(video.title, "B")
        self.assertEqual(video.video_url, "C")
        self.assertEqual(video.img_url, "D")
        self.assertEqual(video.web_url, "E")
        self.assertEqual(video.date, "F")


class VideoParserTest(unittest.TestCase):
    """Class to test CategoryParser """

    def test_parse_video_count_en(self):
        '''Test function '''
        parser = VideoParser()

        self.assertTrue(parser.parse_video_count_en("https://www.cgtn.com/business") > 0)
        self.assertTrue(parser.parse_video_count_en("https://www.cgtn.com/business/economy.html") > 0)
        self.assertTrue(parser.parse_video_count_en("https://www.cgtn.com/politics") > 0)
        self.assertTrue(parser.parse_video_count_en("https://www.cgtn.com/europe/global-business-europe") > 0)
        self.assertTrue(parser.parse_video_count_en("https://www.cgtn.com/europe") > 0)
        self.assertTrue(parser.parse_video_count_en("https://www.cgtn.com/tech-sci") > 0)
        self.assertTrue(parser.parse_video_count_en("https://www.cgtn.com/nature") > 0)
        self.assertTrue(parser.parse_video_count_en("https://www.cgtn.com/nature/live") > 0)
        self.assertTrue(parser.parse_video_count_en("https://www.cgtn.com/china") > 0)

    def test_parse_videos_en(self):
        '''Test function '''
        parser = VideoParser()
        videos = parser.parse_videos_en("https://www.cgtn.com/business")
        for video in videos:
            self.assertIsNotNone(video.data_id)
            self.assertIsNotNone(video.title)
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.img_url)
            self.assertIsNotNone(video.web_url)
            self.assertIsNotNone(video.date)
            self.assertTrue(video.data_id)
            self.assertTrue(video.title)
            self.assertTrue(video.video_url)
            self.assertTrue(video.img_url)
            self.assertTrue(video.web_url)
            self.assertTrue(video.date)
            self.assertTrue(VideoParserTest.is_valid_m3u8_content(video.video_url))

    @staticmethod
    def is_valid_m3u8_content(url):
        """Helper function to check if m3u8 link is valid """
        try:
            request = requests.get(url, timeout=REQUEST_TIMEOUT)
            request.raise_for_status()
        except:
            return []

        return "#EXTM3U" in request.text

if __name__ == '__main__':
    unittest.main()
