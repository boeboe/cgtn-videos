# pylint: disable=bare-except, unsubscriptable-object
"""Package to test section video parser """
import unittest

from cgtn_videos.other.section import SectionParser, SectionFR
from cgtn_videos.video import Video

class SectionParserTest(unittest.TestCase):
    """Class to test SectionParser """

    def test_parse_section_fr(self):
        '''Test function '''
        parser = SectionParser()
        videos = parser.parse_section_fr(SectionFR.CHINE['id'])
        for video in videos:
            self.assertTrue(isinstance(video, Video))
            self.assertIsNotNone(video.uid)
            self.assertIsNotNone(video.channel_id)
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.img_url)
            self.assertIsNotNone(video.web_url)
            self.assertIsNotNone(video.title)
            # self.assertIsNotNone(video.details) # optional
            self.assertIsNotNone(video.editor)
            self.assertIsNotNone(video.publish_date)
            self.assertTrue(video.uid)
            self.assertTrue(video.channel_id)
            self.assertTrue(video.video_url)
            self.assertTrue(video.img_url)
            self.assertTrue(video.web_url)
            self.assertTrue(video.title)
            # self.assertTrue(video.details) # optional
            self.assertTrue(video.editor)
            self.assertTrue(video.publish_date)


if __name__ == '__main__':
    unittest.main()
