import unittest
from src.ZinckLib import numberToText


class NumberToTextTestCases(unittest.TestCase):

    def test_zero(self):
        result = numberToText(0)
        self.assertEqual(result, "zero")

    def test_invalidType(self):
        with self.assertRaises(TypeError):
            numberToText("a")

    def test_empty(self):
        with self.assertRaises(TypeError):
            numberToText()

    def test_longerNum(self):
        result = numberToText(123)
        self.assertEqual(result, "one hundred twenty three")

    def test_tooLongNum(self):
        with self.assertRaises(TypeError):
            numberToText(9999999999999999999999999999999999999)

    def test_tooSmallNum(self):
        with self.assertRaises(TypeError):
            numberToText(-1)


if __name__ == '__main__':
    unittest.main()
