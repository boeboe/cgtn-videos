# pylint: disable=bare-except, unsubscriptable-object
"""Package to test Section """
import unittest

from cgtn_videos.section import SectionVideo, SectionParser, SectionFR

class SectionTest(unittest.TestCase):
    """Class to test Section """

    def test_constructor(self):
        '''Test function '''
        section = SectionVideo(video_url="A", poster_url="B", detail_url="C", headline="D",
                               abstracts="E", editor="F", date="G")

        self.assertEqual(section.video_url, "A")
        self.assertEqual(section.poster_url, "B")
        self.assertEqual(section.detail_url, "C")
        self.assertEqual(section.headline, "D")
        self.assertEqual(section.abstracts, "E")
        self.assertEqual(section.editor, "F")
        self.assertEqual(section.date, "G")


class SectionParserTest(unittest.TestCase):
    """Class to test CategoryParser """

    def test_parse_videos_en(self):
        '''Test function '''
        parser = SectionParser()
        section_videos = parser.parse_section_fr(SectionFR.EXCLUSIVITES.value['id'])
        for video in section_videos:
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.poster_url)
            self.assertIsNotNone(video.detail_url)
            self.assertIsNotNone(video.headline)
            self.assertIsNotNone(video.editor)
            self.assertIsNotNone(video.date)
            self.assertTrue(video.video_url)
            self.assertTrue(video.poster_url)
            self.assertTrue(video.detail_url)
            self.assertTrue(video.headline)
            self.assertTrue(video.editor)
            self.assertTrue(video.date)

if __name__ == '__main__':
    unittest.main()
