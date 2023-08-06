import unittest
from src.ZinckLib import isAlphabetical


class IsAlphabeticalTestCases(unittest.TestCase):

    def test_empty(self):
        result = isAlphabetical("")
        self.assertEqual(result, True)

    def test_invalidType(self):
        with self.assertRaises(TypeError):
            isAlphabetical(1)

    def test_abc(self):
        result = isAlphabetical("abc")
        self.assertEqual(result, True)

    def test_cba(self):
        result = isAlphabetical("cba")
        self.assertEqual(result, False)
    
    def test_ignoreNonLetters(self):
        result = isAlphabetical("a&b!c")
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
