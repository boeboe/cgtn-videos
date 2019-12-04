"""Package to test programs and top news parser """
import unittest

from cgtn_videos.english.program import ProgramParser
from cgtn_videos.video import Video

class ProgramParserTest(unittest.TestCase):
    """Class to test ProgramParser """

    def test_parse_programs(self):
        '''Test function '''
        parser = ProgramParser()

        videos = parser.parse_programs()
        for video in videos:
            self.assertTrue(isinstance(video, Video))
            self.assertIsNotNone(video.uid)
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.img_url)
            self.assertIsNotNone(video.web_url)
            self.assertIsNotNone(video.title)
            self.assertIsNotNone(video.details)
            self.assertIsNotNone(video.editor)
            self.assertIsNotNone(video.publish_date)
            self.assertTrue(video.uid)
            self.assertTrue(video.video_url)
            self.assertTrue(video.img_url)
            self.assertTrue(video.web_url)
            self.assertTrue(video.title)
            self.assertTrue(video.details)
            self.assertTrue(video.editor)
            self.assertTrue(video.publish_date)

    def test_parse_topnews(self):
        '''Test function '''
        parser = ProgramParser()

        videos = parser.parse_topnews()
        for video in videos:
            self.assertTrue(isinstance(video, Video))
            self.assertIsNotNone(video.uid)
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.img_url)
            self.assertIsNotNone(video.web_url)
            self.assertIsNotNone(video.title)
            self.assertIsNotNone(video.details)
            self.assertIsNotNone(video.editor)
            self.assertIsNotNone(video.publish_date)
            self.assertTrue(video.uid)
            self.assertTrue(video.video_url)
            self.assertTrue(video.img_url)
            self.assertTrue(video.web_url)
            self.assertTrue(video.title)
            self.assertTrue(video.details)
            self.assertTrue(video.editor)
            self.assertTrue(video.publish_date)


if __name__ == '__main__':
    unittest.main()
