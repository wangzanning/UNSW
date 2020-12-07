

def f(word):
    '''
    Recall that if c is an ascii character then ord(c) returns its ascii code.
    Will be tested on nonempty strings of lowercase letters only.

    >>> f('x')
    The longest substring of consecutive letters has a length of 1.
    The leftmost such substring is x.
    >>> f('xy')
    The longest substring of consecutive letters has a length of 2.
    The leftmost such substring is xy.
    >>> f('ababcuvwaba')
    The longest substring of consecutive letters has a length of 3.
    The leftmost such substring is abc.
    >>> f('abbcedffghiefghiaaabbcdefgg')
    The longest substring of consecutive letters has a length of 6.
    The leftmost such substring is bcdefg.
    >>> f('abcabccdefcdefghacdef')
    The longest substring of consecutive letters has a length of 6.
    The leftmost such substring is cdefgh.
    '''
    length = 0
    substring = [[]]
    output = ''
    word = list(word)
    first = word[0]
    substring[-1].append(first)
    for i in word[1:]:
        counter = 0
        second = i
        if ord(second) == ord(first) +1:
            substring[-1].append(second)
        
        else:
            substring.append([second])
        first = second
    for i in substring:
        if len(i) > length:
            length = len(i)
            output = ''.join(i)
        
    print(f'The longest substring of consecutive letters has a length of {length}.')
    print(f'The leftmost such substring is {output}.')
             
             
             
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
