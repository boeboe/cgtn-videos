"""Package to test news category parser """
import unittest

from cgtn_videos.english.newscategory import NewsCategory, NewsCategoryParser

class NewsCategoryTest(unittest.TestCase):
    """Class to test NewsCategory """

    def test_constructor(self):
        '''Test function '''
        category = NewsCategory(key="A", name="B", url="C")

        self.assertEqual(category.key, "A")
        self.assertEqual(category.name, "B")
        self.assertEqual(category.url, "C")


class NewsCategoryParserTest(unittest.TestCase):
    """Class to test NewsCategoryParser """

    def test_parse_categories(self):
        '''Test function '''
        parser = NewsCategoryParser()

        categories = parser.parse_categories()
        for category in categories:
            self.assertTrue(isinstance(category, NewsCategory))
            self.assertIsNotNone(category.key)
            self.assertIsNotNone(category.name)
            self.assertIsNotNone(category.url)
            self.assertTrue(category.key)
            self.assertTrue(category.name)
            self.assertTrue(category.url)
            self.assertTrue("https://www.cgtn.com/" in category.url)

    def test_parse_subcategories(self):
        '''Test function '''
        parser = NewsCategoryParser()

        categories = parser.parse_categories()
        for category in categories:
            subcategories = parser.parse_sub_categories(category.url)
            for subcategory in subcategories:
                self.assertTrue(isinstance(category, NewsCategory))
                self.assertIsNotNone(subcategory.key)
                self.assertIsNotNone(subcategory.name)
                self.assertIsNotNone(subcategory.url)
                self.assertTrue(subcategory.key)
                self.assertTrue(subcategory.name)
                self.assertTrue(subcategory.url)
                self.assertTrue("https://www.cgtn.com/" in subcategory.url)


if __name__ == '__main__':
    unittest.main()
