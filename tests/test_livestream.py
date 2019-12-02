"""Package to test Livestreams """
import unittest

from cgtn_videos.livestream import Livestream, LivestreamParser
from cgtn_videos.region import Region

class LivestreamTest(unittest.TestCase):
    """Class to test Livestream """

    def test_constructor(self):
        '''Test function '''
        livestream = Livestream(video_url="A", program="B", start="C", end="D")
        self.assertEqual(livestream.video_url, "A")
        self.assertEqual(livestream.program, "B")
        self.assertEqual(livestream.start, "C")
        self.assertEqual(livestream.end, "D")

class LivestreamParserTest(unittest.TestCase):
    """Class to test LivestreamParser """

    def test_parse(self):
        '''Test function '''
        parser = LivestreamParser()

        for region in Region:
            livestream = parser.parse(region)
            self.assertIsNotNone(livestream.video_url)
            self.assertIsNotNone(livestream.program)
            self.assertIsNotNone(livestream.start)
            self.assertIsNotNone(livestream.end)
            self.assertTrue(livestream.video_url)
            self.assertTrue(livestream.program)
            self.assertTrue(livestream.start)
            self.assertTrue(livestream.end)