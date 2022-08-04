import unittest

from translator import englishtofrench, englishtogerman

class TestEnglishToFrench(unittest.TestCase):
    def test1(self):
        self.assertEqual(englishtofrench("hello"),"Bonjour")
        self.assertEqual(englishtofrench("welcome"),"Bienvenue")
        self.assertEqual(englishtofrench("love"),"Amour")
        #self.assertEqual(englishtofrench(""),"error")

class TestEnglishToGerman(unittest.TestCase):
    def test1(self):
        self.assertEqual(englishtogerman("hello"),"Hallo")
        self.assertEqual(englishtogerman("welcome"),"Begrüßung")
        self.assertEqual(englishtogerman("love"),"Liebe")

unittest.main()