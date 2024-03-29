# pylint: disable=bare-except, broad-except, superfluous-parens
"""Package to test Videos """
import unittest

from cgtn_videos.video import Video

class VideoTest(unittest.TestCase):
    """Class to test Video """

    def test_constructor(self):
        '''Test function '''
        video = Video(uid="A", channel_id="B", video_url="C", img_url="D", web_url="E",
                      title="F", details="G", editor="H", publish_date="I", start_date="J",
                      end_date="K")

        self.assertEqual(video.uid, "A")
        self.assertEqual(video.channel_id, "B")
        self.assertEqual(video.video_url, "C")
        self.assertEqual(video.img_url, "D")
        self.assertEqual(video.web_url, "E")
        self.assertEqual(video.title, "F")
        self.assertEqual(video.details, "G")
        self.assertEqual(video.editor, "H")
        self.assertEqual(video.publish_date, "I")
        self.assertEqual(video.start_date, "J")
        self.assertEqual(video.end_date, "K")

    def test_equal(self):
        '''Test function '''
        video1 = Video(uid="A", video_url="B")
        video2 = Video(uid="A", video_url="B", img_url="C")
        video3 = Video(uid="AA", video_url="BB", img_url="CC", web_url="DD")
        video4 = Video(video_url="BB", img_url="CCC", web_url="DDD")

        self.assertEqual(video1, video2)
        self.assertEqual(video3, video4)
        self.assertNotEqual(video1, video3)
        self.assertNotEqual(video1, video4)
        self.assertNotEqual(video2, video3)
        self.assertNotEqual(video2, video4)

    def test_hash(self):
        '''Test function '''
        video_set = set()
        video1 = Video(uid="A", video_url="B")
        video2 = Video(uid="A", video_url="B", img_url="C")
        video3 = Video(uid="AA", video_url="BB", img_url="CC", web_url="DD")
        video4 = Video(video_url="BB", img_url="CCC", web_url="DDD")

        video_set.add(video1)
        self.assertEqual(len(video_set), 1)
        video_set.add(video2)
        self.assertEqual(len(video_set), 1)
        video_set.add(video3)
        self.assertEqual(len(video_set), 2)
        video_set.add(video4)
        self.assertEqual(len(video_set), 2)


if __name__ == '__main__':
    unittest.main()
