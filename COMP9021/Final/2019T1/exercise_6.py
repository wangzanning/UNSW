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
    # print()
    output = [[]]
    start = ord('a')
    end = ord('z')
    for i in range(height):
        
        while True:
        
            output[-1].append(chr(start))
            start+=1
            if start == ord('z')+1:
                start = ord('a')
            if len(output[-1]) == width:
                break
        output.append([])

    output.remove([])    
    for i in range(len(output)):
        if i % 2 == 1:
            output[i] = list(reversed(output[i]))
    
    for i in range(len(output)):
        line = ''.join(output[i])
        print(line)


    
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE
    # 1.两种,边打印，边输出 2.放到list 一起打印

if __name__ == '__main__':
    import doctest
    doctest.testmod()
