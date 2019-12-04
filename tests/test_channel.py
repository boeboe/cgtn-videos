"""Package to test channel video parser """
import unittest

from cgtn_videos.channel import ChannelParser, Channel
from cgtn_videos.video import Video

class ChannelParserTest(unittest.TestCase):
    """Class to test ChannelParser """

    def test_parse_current_live(self):
        '''Test function '''
        parser = ChannelParser()

        video = parser.parse_current_live(Channel.ENGLISH)
        self.assertTrue(isinstance(video, Video))
        self.assertIsNotNone(video.uid)
        self.assertIsNotNone(video.video_url)
        self.assertIsNotNone(video.title)
        self.assertIsNotNone(video.start_date)
        self.assertIsNotNone(video.end_date)
        self.assertTrue(video.uid)
        self.assertTrue(video.video_url)
        self.assertTrue(video.title)
        self.assertTrue(video.start_date)
        self.assertTrue(video.end_date)

    def test_parse_history_count(self):
        '''Test function '''
        parser = ChannelParser()
        program_count = parser.parse_history_count(Channel.ARABIC)
        self.assertTrue(program_count > 0)

    def test_parse_history_by_month(self):
        '''Test function '''
        parser = ChannelParser()

        videos = parser.parse_history_by_month(Channel.SPANISH, year=2019, month=1, day=1)
        self.assertTrue(videos)
        for video in videos:
            self.assertTrue(isinstance(video, Video))
            self.assertIsNotNone(video.uid)
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.title)
            self.assertIsNotNone(video.start_date)
            self.assertIsNotNone(video.end_date)
            self.assertTrue(video.uid)
            self.assertTrue(video.video_url)
            self.assertTrue(video.title)
            self.assertTrue(video.start_date)
            self.assertTrue(video.end_date)

    def test_parse_history_from_now(self):
        '''Test function '''
        parser = ChannelParser()

        videos = parser.parse_history_from_now(Channel.RUSSIAN, hours=3)
        self.assertTrue(videos)
        for video in videos:
            self.assertTrue(isinstance(video, Video))
            self.assertIsNotNone(video.uid)
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.title)
            self.assertIsNotNone(video.start_date)
            self.assertIsNotNone(video.end_date)
            self.assertTrue(video.uid)
            self.assertTrue(video.video_url)
            self.assertTrue(video.title)
            self.assertTrue(video.start_date)
            self.assertTrue(video.end_date)


if __name__ == '__main__':
    unittest.main()
