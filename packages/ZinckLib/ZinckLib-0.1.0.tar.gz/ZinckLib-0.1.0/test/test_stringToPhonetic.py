import unittest
from src.ZinckLib import stringToPhonetic


class StringToPhoneticTestCases(unittest.TestCase):

    def test_empty(self):
        result = stringToPhonetic("")
        self.assertEqual(result, [])

    def test_invalidType(self):
        with self.assertRaises(TypeError):
            stringToPhonetic(1)

    def test_oneChar(self):
        result = stringToPhonetic("a")
        self.assertEqual(result, ["Alfa"])

    def test_string(self):
        result = stringToPhonetic("python")
        self.assertEqual(result, ['Papa', 'Yankee', 'Tango', 'Hotel', 'Oscar', 'November'])

    def test_stringWithCapital(self):
        result = stringToPhonetic("Python")
        self.assertEqual(result, ['Papa', 'Yankee', 'Tango', 'Hotel', 'Oscar', 'November'])

    def test_stringGarbage(self):
        result = stringToPhonetic("Py2t^ho0n!")
        self.assertEqual(result, ['Papa', 'Yankee', '2', 'Tango', '^', 'Hotel', 'Oscar', '0', 'November', '!'])


if __name__ == '__main__':
    unittest.main()
