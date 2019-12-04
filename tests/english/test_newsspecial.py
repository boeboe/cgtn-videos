"""Package to test news specials parser """
import unittest

from cgtn_videos.english.newsspecial import NewsSpecial, NewsSpecialParser

class NewsSpecialTest(unittest.TestCase):
    """Class to test NewsSpecial """

    def test_constructor(self):
        '''Test function '''
        special = NewsSpecial(key="A", name="B", url="C", img_url="D")

        self.assertEqual(special.key, "A")
        self.assertEqual(special.name, "B")
        self.assertEqual(special.url, "C")
        self.assertEqual(special.img_url, "D")


class NewsSpecialParserTest(unittest.TestCase):
    """Class to test NewsSpecialParser """

    def test_parse_categories(self):
        '''Test function '''
        parser = NewsSpecialParser()

        specials = parser.parse_specials("2019")
        self.assertTrue(specials)
        for special in specials:
            self.assertTrue(isinstance(special, NewsSpecial))
            self.assertIsNotNone(special.key)
            self.assertIsNotNone(special.name)
            self.assertIsNotNone(special.url)
            self.assertIsNotNone(special.img_url)
            self.assertTrue(special.key)
            self.assertTrue(special.name)
            self.assertTrue(special.url)
            self.assertTrue(special.img_url)


if __name__ == '__main__':
    unittest.main()
