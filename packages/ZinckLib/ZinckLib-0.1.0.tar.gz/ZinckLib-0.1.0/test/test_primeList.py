import unittest
from src.ZinckLib import primeList


class PrimeListTestCases(unittest.TestCase):

    def test_zero(self):
        result = primeList(0)
        self.assertEqual(result, [])

    def test_one(self):
        result = primeList(1)
        self.assertEqual(result, [])

    def test_ten(self):
        result = primeList(10)
        self.assertEqual(result, [2, 3, 5, 7])

    def test_negativeOne(self):
        with self.assertRaises(TypeError):
            primeList(-1)

    def test_invalidType(self):
        with self.assertRaises(TypeError):
            primeList("a")


if __name__ == '__main__':
    unittest.main()
