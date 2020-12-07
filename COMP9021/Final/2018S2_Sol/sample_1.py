from itertools import groupby


def remove_consecutive_duplicates(word):
    '''
    >>> remove_consecutive_duplicates('')
    ''
    >>> remove_consecutive_duplicates('a')
    'a'
    >>> remove_consecutive_duplicates('ab')
    'ab'
    >>> remove_consecutive_duplicates('aba')
    'aba'
    >>> remove_consecutive_duplicates('aaabbbbbaaa')
    'aba'
    >>> remove_consecutive_duplicates('abcaaabbbcccabc')
    'abcabcabc'
    >>> remove_consecutive_duplicates('aaabbbbbaaacaacdddd')
    'abacacd'
    '''
    # Insert your code here (the output is returned, not printed out)               
    result = ''
    if word:
        # first method
        result = word[0]
        for char in word[1:]:
            if result[-1] != char:
                result += char

        # second method
        result = ''.join([k for k, g in groupby(word)])

    return result


if __name__ == '__main__':
    import doctest

    doctest.testmod()
