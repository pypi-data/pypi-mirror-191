import unittest
from src.ZinckLib import splitString


class SplitStringTestCases(unittest.TestCase):

    def test_empty(self):
        result = splitString("")
        self.assertEqual(result, [])

    def test_string(self):
        result = splitString("python")
        self.assertEqual(result, ["p", "y", "t", "h", "o", "n"])

    def test_shortString(self):
        result = splitString("p")
        self.assertEqual(result, ["p"])

    def test_invalidType(self):
        with self.assertRaises(TypeError):
            splitString(1)


if __name__ == '__main__':
    unittest.main()
