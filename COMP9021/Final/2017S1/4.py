import sys
from math import sqrt

def get_all_divisor(n):
    if n == 1:
        return [1]
    result = []
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            result.append(i)
            result.append(n // i)
    return result

def f(n):
    '''
    A number n is deficient if the sum of its proper divisors,
    1 included and itself excluded,
    is strictly smaller than n.
    
    >>> f(1)
    1 is deficient
    >>> f(2)
    2 is deficient
    >>> f(3)
    3 is deficient
    >>> f(6)
    6 is not deficient
    >>> f(29)
    29 is deficient
    >>> f(30)
    30 is not deficient
    >>> f(47)
    47 is deficient
    >>> f(48)
    48 is not deficient
    '''
    #input your code

    divisor_list = get_all_divisor(n)


    sum_divi = 0
    divisor_list.append(1)
    for i in divisor_list:
        sum_divi += i

    if  n ==1 or sum_divi < n:
        print(f'{n} is deficient')
    else:
        print(f'{n} is not deficient')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
