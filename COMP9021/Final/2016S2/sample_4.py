
def is_heterosquare(square):
    '''
    A heterosquare of order n is an arrangement of the integers 1 to n**2 in a square,
    such that the rows, columns, and diagonals all sum to DIFFERENT values.
    In contrast, magic squares have all these sums equal.
    
    
    >>> is_heterosquare([[1, 2, 3],\
                         [8, 9, 4],\
                         [7, 6, 5]])
    True
    >>> is_heterosquare([[1, 2, 3],\
                         [9, 8, 4],\
                         [7, 6, 5]])
    False
    >>> is_heterosquare([[2, 1, 3, 4],\
                         [5, 6, 7, 8],\
                         [9, 10, 11, 12],\
                         [13, 14, 15, 16]])
    True
    >>> is_heterosquare([[1, 2, 3, 4],\
                         [5, 6, 7, 8],\
                         [9, 10, 11, 12],\
                         [13, 14, 15, 16]])
    False
    '''
    n = len(square)
    if any(len(line) != n for line in square):
        return False
    # Insert your code here
    new_list = []
    new_list_2 = [[]]
    for i in range(1,n**2+1):
        new_list.append(i)
    new_list_2[0] = new_list[:4]
    new_list = new_list[4:]
    for j in range(n-1):
        new_list_2.append(new_list[:4])
        new_list = new_list[4:]

    sum_list = []
    a = 0
    b = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                a += new_list_2[i][j]
            if j == n-i:
                b += new_list_2[i][j-1]
    sum_list.append(a)
    sum_list.append(b)

    for i in range(n):
        print(f'{new_list_2[i]}, \\')
    print(sum_list)
                

# Possibly define other functions

    
if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    is_heterosquare([[1, 2, 3, 4], \
                     [5, 6, 7, 8], \
                     [9, 10, 11, 12], \
                     [13, 14, 15, 16]])
    False
