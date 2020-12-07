
from math import sqrt

def f(n, d):
    '''
    >>> f(2, 1)
    1 is not a proper factor of 2.
    >>> f(2, 2)
    2 is not a proper factor of 2.
    >>> f(16, 2)
    2 is a proper factor of 16 of mutiplicity 4.
    >>> f(100, 20)
    20 is a proper factor of 100 of mutiplicity 1.
    >>> f(8 ** 7 * 3 ** 5 * 11 ** 2, 8)
    8 is a proper factor of 61662560256 of mutiplicity 7.
    >>> f(3 ** 3 * 11 * 13 ** 2 * 40 ** 6, 8)
    8 is a proper factor of 205590528000000 of mutiplicity 6.
    '''
    counter = 0
    shit = n
    if n ==2:
        print(f'{d} is not a proper factor of {n}.')
    
    else:
        while True:
            a,b = divmod(n,d)
            if b ==0:
                counter += 1
                n = a
            else:
                break
        print(f'{d} is a proper factor of {shit} of mutiplicity {counter}.')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
