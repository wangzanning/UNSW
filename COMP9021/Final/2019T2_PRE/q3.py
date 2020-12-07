

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
    desired_length = 0
    desired_substring = ''
    # Insert your code here

    word = list(word)
    output_list = [[]]
    first = word[0]
    output_list[-1] += first
    
    for i in word[1:]:
        second = i
        if ord(second) - ord(first) == 1:
            output_list[-1]+=(second)
        else:
            output_list.append([second])

        first = second


    
    desired_length = 0
    output = [''.join(i) for i in output_list]
   

    for i in output:
        if len(i) > desired_length:
            desired_length = len(i)
            desired_substring = i
    

    print(f'The longest substring of consecutive letters has a length of {desired_length}.')
    print(f'The leftmost such substring is {desired_substring}.')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
