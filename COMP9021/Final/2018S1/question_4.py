import sys
from math import sqrt
from itertools import compress


def f(n):
    '''
    Won't be tested for n greater than 10_000_000
    
    >>> f(3)
    The largest prime strictly smaller than 3 is 2.
    >>> f(10)
    The largest prime strictly smaller than 10 is 7.
    >>> f(20)
    The largest prime strictly smaller than 20 is 19.
    >>> f(210)
    The largest prime strictly smaller than 210 is 199.
    >>> f(1318)
    The largest prime strictly smaller than 1318 is 1307.
    '''
    if n <= 2:
        sys.exit()
    largest_prime_strictly_smaller_than_n = 0
    # Insert your code here

    def is_prime(n):
        if n == 2:
            return True
        if n % 2 ==1:
            return all(n % d for d in range(3,round(sqrt(n))+1,2))
    prime = []
    for i in range(2,n):
        if is_prime(i):
            prime.append(i)
    output = prime [-1]
    print(f'The largest prime strictly smaller than {n} is {output}.')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
