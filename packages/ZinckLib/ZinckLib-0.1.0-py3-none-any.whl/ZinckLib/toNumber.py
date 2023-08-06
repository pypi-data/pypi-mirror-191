from src.ZinckLib import splitString


def toNumber(toConv: str):
    """
    converts a string to a list of ints representing the number(i.e. 1 = a, 2 = b, ..., 26 = z) with 0 representing
    any spaces and any non letter values not being converted.

    :param toConv: The string to be converted.
    :type toConv: str

    :return: the string/list/number that represents the given string.
    :rtype: a list of ints
    """
    if type(toConv) is not str:
        raise TypeError('Only strings are allowed')

    toConv = toConv.upper()
    toConv = splitString(toConv)
    out = []
    for char in toConv:
        val = ord(char) - 64
        if 0 < val <= 26:
            out.append(val)
            continue
        elif val == -32:
            out.append(0)
            continue
        out.append(char)
    return out
