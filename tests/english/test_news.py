# pylint: disable=bare-except, broad-except, superfluous-parens
"""Package to test news video parser """
import unittest

from cgtn_videos.english.news import NewsParser
from cgtn_videos.video import Video

class NewsParserTest(unittest.TestCase):
    """Class to test NewsParser """

    def test_parse_video_count(self):
        '''Test function '''
        parser = NewsParser()

        self.assertTrue(parser.parse_video_count("https://www.cgtn.com/business") > 0)
        self.assertTrue(parser.parse_video_count("https://www.cgtn.com/business/economy.html") > 0)
        self.assertTrue(parser.parse_video_count("https://www.cgtn.com/nature") > 0)
        self.assertTrue(parser.parse_video_count("https://www.cgtn.com/nature/live") > 0)
        self.assertTrue(parser.parse_video_count("https://www.cgtn.com/china") > 0)

    def test_parse_videos(self):
        '''Test function '''
        parser = NewsParser()
        videos = parser.parse_videos("https://www.cgtn.com/business")
        for video in videos:
            self.assertTrue(isinstance(video, Video))
            self.assertIsNotNone(video.uid)
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.img_url)
            self.assertIsNotNone(video.web_url)
            self.assertIsNotNone(video.title)
            self.assertIsNotNone(video.publish_date)
            self.assertTrue(video.uid)
            self.assertTrue(video.video_url)
            self.assertTrue(video.img_url)
            self.assertTrue(video.web_url)
            self.assertTrue(video.title)
            self.assertTrue(video.publish_date)


if __name__ == '__main__':
    unittest.main()
