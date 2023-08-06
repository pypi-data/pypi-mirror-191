import unittest
from src.ZinckLib import toNumber


class ToNumbersTestCases(unittest.TestCase):

    def test_empty(self):
        result = toNumber("")
        self.assertEqual(result, [])

    def test_space(self):
        result = toNumber(" ")
        self.assertEqual(result, [0])

    def test_singleCharA(self):
        result = toNumber("a")
        self.assertEqual(result, [1])

    def test_singleCharZ(self):
        result = toNumber("z")
        self.assertEqual(result, [26])

    def test_MultipleCharABC(self):
        result = toNumber("abc")
        self.assertEqual(result, [1, 2, 3])

    def test_invalidType(self):
        with self.assertRaises(TypeError):
            toNumber(1)


if __name__ == '__main__':
    unittest.main()