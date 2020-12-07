# You might find the ord() function useful.

def longest_leftmost_sequence_of_consecutive_letters(word):
    '''
    You can assume that "word" is a string of
    nothing but lowercase letters.
    
    >>> longest_leftmost_sequence_of_consecutive_letters('')
    ''
    >>> longest_leftmost_sequence_of_consecutive_letters('a')
    'a'
    >>> longest_leftmost_sequence_of_consecutive_letters('zuba')
    'z'
    >>> longest_leftmost_sequence_of_consecutive_letters('ab')
    'ab'
    >>> longest_leftmost_sequence_of_consecutive_letters('bcab')
    'bc'
    >>> longest_leftmost_sequence_of_consecutive_letters('aabbccddee')
    'ab'
    >>> longest_leftmost_sequence_of_consecutive_letters('aefbxyzcrsdt')
    'xyz'
    >>> longest_leftmost_sequence_of_consecutive_letters('efghuvwijlrstuvabcde')
    'rstuv'
    '''
 
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE                
    desired_length = 0
    desired_substring = ''
    word = list(word)
    output_list = [[]]
    if len(word)== 0:
        return ''
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

    return desired_substring
if __name__ == '__main__':
    import doctest
    doctest.testmod()
