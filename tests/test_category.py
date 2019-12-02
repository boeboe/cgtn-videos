"""Package to test Categories """
import unittest

from cgtn_videos.category import Category, CategoryParser

class CategoryTest(unittest.TestCase):
    """Class to test Category """

    def test_constructor(self):
        '''Test function '''
        category = Category(key="A", name="B", url="C")

        self.assertEqual(category.key, "A")
        self.assertEqual(category.name, "B")
        self.assertEqual(category.url, "C")


class CategoryParserTest(unittest.TestCase):
    """Class to test CategoryParser """

    def test_parse_categories(self):
        '''Test function '''
        parser = CategoryParser()

        categories = parser.parse_categories()
        for category in categories:
            self.assertIsNotNone(category.key)
            self.assertIsNotNone(category.name)
            self.assertIsNotNone(category.url)
            self.assertTrue(category.key)
            self.assertTrue(category.name)
            self.assertTrue(category.url)
            self.assertTrue("https://www.cgtn.com/" in category.url)

    def test_parse_subcategories(self):
        '''Test function '''
        parser = CategoryParser()

        categories = parser.parse_categories()
        for category in categories:
            subcategories = parser.parse_sub_categories(category.url)
            for subcategory in subcategories:
                self.assertIsNotNone(subcategory.key)
                self.assertIsNotNone(subcategory.name)
                self.assertIsNotNone(subcategory.url)
                self.assertTrue(subcategory.key)
                self.assertTrue(subcategory.name)
                self.assertTrue(subcategory.url)
                self.assertTrue("https://www.cgtn.com/" in subcategory.url)
