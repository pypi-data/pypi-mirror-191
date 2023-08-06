def splitString(string: str):
    """
    Splits a string into a list of chars

    :param string: The string to split.
    :type string: str

    :return: the string split into individual chars
    :rtype: list of strings
    """
    if type(string) is not str:
        raise TypeError('Only strings are allowed')
    return [char for char in string]
