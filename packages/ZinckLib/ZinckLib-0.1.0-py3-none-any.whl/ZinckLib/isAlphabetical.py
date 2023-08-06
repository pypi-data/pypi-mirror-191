def isAlphabetical(toCheck: str):
    """
    Checks to see if a given string is in alphabetical order

    :param toCheck: the string to be checked
    :type toCheck: str

    :return: true or false if it is alphabetical
    :rtype: boolean
    """
    if type(toCheck) is not str:
        raise TypeError('Only strings are allowed')
    toCheck = toCheck.lower()
    lastOrd = 96
    for char in toCheck:
        orded = ord(char)
        if 97 <= orded <= 122:
            if lastOrd > orded:
                return False
            lastOrd = orded
    return True
