import unittest
from src.ZinckLib import toLetter


class ToLetterTestCases(unittest.TestCase):

    def test_empty(self):
        result = toLetter([])
        self.assertEqual(result, "")

    def test_singleCharA(self):
        result = toLetter([1])
        self.assertEqual(result, "a")

    def test_singleCharZ(self):
        result = toLetter([26])
        self.assertEqual(result, "z")

    def test_space(self):
        result = toLetter([0])
        self.assertEqual(result, " ")

    def test_multipleCharABC(self):
        result = toLetter([1, 2, 3])
        self.assertEqual(result, "abc")

    def test_invalidType(self):
        with self.assertRaises(TypeError):
            toLetter("p")

    def test_invalidTypeAloneInList(self):
        with self.assertRaises(TypeError):
            toLetter(["p"])

    def test_invalidTypeMixedInList(self):
        with self.assertRaises(TypeError):
            toLetter([1, 2, "p"])



if __name__ == '__main__':
    unittest.main()
