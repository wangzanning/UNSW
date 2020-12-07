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

    max_string = ''
    if word:
        first = word[0]
        max_length = 1
        temp_length = 1
        max_string = first
        temp_string = first
        # ab
        #
        for second in word[1:]:
            if ord(first) + 1 == ord(second):
                temp_length +=1
                temp_string += second
            else:
                max_length = max(max_length,temp_length)
                if len(temp_string) > len(max_string):
                    max_string = temp_string
                temp_length = 1
                temp_string = second

            first = second


        max_length = max(max_length, temp_length)

        if len(temp_string) > len(max_string):
            max_string = temp_string


    return max_string


if __name__ == '__main__':
    import doctest
    doctest.testmod()
