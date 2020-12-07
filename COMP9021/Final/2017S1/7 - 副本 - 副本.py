''' ord(c) returns the encoding of character c.
    chr(e) returns the character encoded by e.
'''
def f(n):
    '''
    >>> f(1)
    A
    >>> f(2)
     A
    CBC
    >>> f(3)
      A
     CBC
    EDCDE
    >>> f(4)
       A
      CBC
     EDCDE
    GFEDEFG
    >>> f(30)
                                 A
                                CBC
                               EDCDE
                              GFEDEFG
                             IHGFEFGHI
                            KJIHGFGHIJK
                           MLKJIHGHIJKLM
                          ONMLKJIHIJKLMNO
                         QPONMLKJIJKLMNOPQ
                        SRQPONMLKJKLMNOPQRS
                       UTSRQPONMLKLMNOPQRSTU
                      WVUTSRQPONMLMNOPQRSTUVW
                     YXWVUTSRQPONMNOPQRSTUVWXY
                    AZYXWVUTSRQPONOPQRSTUVWXYZA
                   CBAZYXWVUTSRQPOPQRSTUVWXYZABC
                  EDCBAZYXWVUTSRQPQRSTUVWXYZABCDE
                 GFEDCBAZYXWVUTSRQRSTUVWXYZABCDEFG
                IHGFEDCBAZYXWVUTSRSTUVWXYZABCDEFGHI
               KJIHGFEDCBAZYXWVUTSTUVWXYZABCDEFGHIJK
              MLKJIHGFEDCBAZYXWVUTUVWXYZABCDEFGHIJKLM
             ONMLKJIHGFEDCBAZYXWVUVWXYZABCDEFGHIJKLMNO
            QPONMLKJIHGFEDCBAZYXWVWXYZABCDEFGHIJKLMNOPQ
           SRQPONMLKJIHGFEDCBAZYXWXYZABCDEFGHIJKLMNOPQRS
          UTSRQPONMLKJIHGFEDCBAZYXYZABCDEFGHIJKLMNOPQRSTU
         WVUTSRQPONMLKJIHGFEDCBAZYZABCDEFGHIJKLMNOPQRSTUVW
        YXWVUTSRQPONMLKJIHGFEDCBAZABCDEFGHIJKLMNOPQRSTUVWXY
       AZYXWVUTSRQPONMLKJIHGFEDCBABCDEFGHIJKLMNOPQRSTUVWXYZA
      CBAZYXWVUTSRQPONMLKJIHGFEDCBCDEFGHIJKLMNOPQRSTUVWXYZABC
     EDCBAZYXWVUTSRQPONMLKJIHGFEDCDEFGHIJKLMNOPQRSTUVWXYZABCDE
    GFEDCBAZYXWVUTSRQPONMLKJIHGFEDEFGHIJKLMNOPQRSTUVWXYZABCDEFG
    '''
    if n <1:
        return

    # 1. A开始
    # 2.从中间开始，对称
    # 3.每行都是奇数
    # 4.左边空格数
    # 5.反转
    # 6.Z 后面是A

    # 打印有两种，一种是放到列表
    # 边打印边输出

    for h in range(n):
        start = ord('A')+(h % 26)
        line = ''
        for j in range(n-h-1):
            print(' ',end = '')
        for j in range(h+1):
            line += chr(start)
            start +=1 
            if start == ord('Z')+1:
                start = ord('A')
            
        
        print(line[1:][::-1],end = '')
        print(line,end='')
        print('')
            


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # f(3)
