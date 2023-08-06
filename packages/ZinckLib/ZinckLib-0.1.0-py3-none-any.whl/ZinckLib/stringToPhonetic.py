def stringToPhonetic(toConv: str):
    """
    Converts a string to a list of strings where all the letters are replaced with their representation in the NATO
    phonetic alphabet according to: https://en.wikipedia.org/wiki/NATO_phonetic_alphabet#Tables

    :param toConv: The string to be converted.
    :type toConv: str

    :return: the phonetic version of the original string
    :rtype: list of strings
    """
    if type(toConv) is not str:
        raise TypeError('Only strings are allowed')

    phoneticDict = {
        "a": "Alfa",
        "b": "Bravo",
        "c": "Charlie",
        "d": "Delta",
        "e": "Echo",
        "f": "Foxtrot",
        "g": "Golf",
        "h": "Hotel",
        "i": "India",
        "j": "Juliett",
        "k": "Kilo",
        "l": "Lima",
        "m": "Mike",
        "n": "November",
        "o": "Oscar",
        "p": "Papa",
        "q": "Quebec",
        "r": "Romeo",
        "s": "Sierra",
        "t": "Tango",
        "u": "Uniform",
        "v": "Victor",
        "w": "Whiskey",
        "x": "X-ray",
        "y": "Yankee",
        "z": "Zulu",
    }
    out = []
    toConv = toConv.lower()
    for char in toConv:
        val = ord(char) - 96
        if 0 < val <= 26:
            out.append(phoneticDict[char])
        else:
            out.append(char)

    return out
