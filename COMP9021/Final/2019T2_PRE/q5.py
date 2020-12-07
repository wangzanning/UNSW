# ord(c) returns the encoding of character c.
# chr(e) returns the character encoded by e.


def rectangle(width, height):
    '''
    Displays a rectangle by outputting lowercase letters, starting with a,
    in a "snakelike" manner, from left to right, then from right to left,
    then from left to right, then from right to left, wrapping around when z is reached.
    
    >>> rectangle(1, 1)
    a
    >>> rectangle(2, 3)
    ab
    dc
    ef
    >>> rectangle(3, 2)
    abc
    fed
    >>> rectangle(17, 4)
    abcdefghijklmnopq
    hgfedcbazyxwvutsr
    ijklmnopqrstuvwxy
    ponmlkjihgfedcbaz
    '''
    start = ord('a')
    input_list = []
    for i in range(width * height):
        input_list.append(chr(start))
        start += 1
        if start == ord('z')+1:
            start = ord('a')
    input_list = ''.join(input_list)

    for i in range(height):
        if i% 2 ==0:
            print(input_list[:width])
            input_list = input_list[width:]
        else:
            print(input_list[:width][::-1])
            input_list = input_list[width:]

    
        
    
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE


if __name__ == '__main__':
    import doctest
    doctest.testmod()
