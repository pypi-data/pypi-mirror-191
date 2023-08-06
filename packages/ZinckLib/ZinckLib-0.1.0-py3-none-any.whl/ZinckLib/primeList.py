def primeList(maxVal: int):
    """
    takes in an integer and uses the sieve of eratosthenes to calculate and return a list of prime numbers less than or
    equal to the provided number

    :param maxVal: The maximum value for the prime list
    :type maxVal: int

    :return: A list of prime numbers less than or equal to a specified value
    :rtype: list of ints
    """
    if type(maxVal) is not int:
        raise TypeError('Only positive integers are allowed')
    if maxVal < 0:
        raise TypeError('Only positive integers are allowed')

    intList = list(range(2, maxVal))
    maxCheck = int(maxVal ** 0.5)
    for i in range(2, maxCheck+1):
        for ints in intList:
            if ints % i == 0 and not(ints == i):
                intList.remove(ints)

    return intList


