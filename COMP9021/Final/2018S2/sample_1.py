
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

    output = []
    word = list(word)
    if word:
        output.append(word[0])
        for i in word[1:]:
            if i != output[-1]:
                output.append(i)
            else:
                pass
        output = ''.join(output)
        return output
    else:
        return ''
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()

