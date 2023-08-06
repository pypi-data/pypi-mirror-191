def toLetter(valList: list[int]):
    """
    Takes a list of ints and combines them into one string based (1 = a, 2 = b, ..., 26 = z) with spaces being 0

    :param valList: The list of ints to convert
    :type valList: list of ints

    :return: this list combined into a string
    :rtype: string
    """
    if type(valList) is not list:
        raise TypeError('Only integer lists are allowed')

    output = ""
    for val in valList:
        if type(val) is not int:
            raise TypeError('Only integer lists are allowed')
        if 0 < val <= 26:
            val = chr(96+val)
        elif val == 0:
            val = " "
        output = output + str(val)
    return output
