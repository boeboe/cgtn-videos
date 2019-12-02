"""Package to test Programs """
import unittest

from cgtn_videos.program import ProgramVideo, ProgramParser

class ProgramVideoTest(unittest.TestCase):
    """Class to test ProgramVideo """

    def test_constructor(self):
        '''Test function '''
        programvideo = ProgramVideo(video_url="A",
                                    poster_url="B",
                                    detail_url="C",
                                    share_url="D",
                                    headline="E",
                                    publish_time="F",
                                    editor="G")

        self.assertEqual(programvideo.video_url, "A")
        self.assertEqual(programvideo.poster_url, "B")
        self.assertEqual(programvideo.detail_url, "C")
        self.assertEqual(programvideo.share_url, "D")
        self.assertEqual(programvideo.headline, "E")
        self.assertEqual(programvideo.publish_time, "F")
        self.assertEqual(programvideo.editor, "G")

class ProgramParserTest(unittest.TestCase):
    """Class to test ProgramParser """

    def test_parse(self):
        '''Test function '''
        parser = ProgramParser()

        programvideos = parser.parse()
        for video in programvideos:
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.poster_url)
            self.assertIsNotNone(video.detail_url)
            self.assertIsNotNone(video.share_url)
            self.assertIsNotNone(video.headline)
            self.assertIsNotNone(video.publish_time)
            self.assertIsNotNone(video.editor)

            self.assertTrue(video.video_url)
            self.assertTrue(video.poster_url)
            self.assertTrue(video.detail_url)
            self.assertTrue(video.share_url)
            self.assertTrue(video.headline)
            self.assertTrue(video.publish_time)
            self.assertTrue(video.editor)

if __name__ == '__main__':
    unittest.main()
