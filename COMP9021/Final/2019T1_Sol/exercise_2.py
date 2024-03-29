
def rearrange(L, from_first = True):
    '''
    Returns a new list consisting of:
    * in case "from_first" is True:
         L's first member if it exists, then
         L's last member if it exists, then
         L's second member if it exists, then
         L's second last member if it exists, then
         L's third member if it exists...
    * in case "from_first" is False:
         L's last member if it exists, then
         L's first member if it exists, then
         L's second last member if it exists, then
         L's second member if it exists, then
         L's third last member if it exists...

    >>> L = []
    >>> rearrange(L), L
    ([], [])
    >>> L = [10]
    >>> rearrange(L, False), L
    ([10], [10])
    >>> L = [10, 20]
    >>> rearrange(L), L
    ([10, 20], [10, 20])
    >>> L = [10, 20, 30]
    >>> rearrange(L), L
    ([10, 30, 20], [10, 20, 30])
    >>> L = [10, 20, 30, 40]
    >>> rearrange(L, False), L
    ([40, 10, 30, 20], [10, 20, 30, 40])
    >>> L = [10, 20, 30, 40, 50]
    >>> rearrange(L, False), L
    ([50, 10, 40, 20, 30], [10, 20, 30, 40, 50])
    >>> L = [10, 20, 30, 40, 50, 60]
    >>> rearrange(L), L
    ([10, 60, 20, 50, 30, 40], [10, 20, 30, 40, 50, 60])
    >>> L = [10, 20, 30, 40, 50, 60, 70]
    >>> rearrange(L), L
    ([10, 70, 20, 60, 30, 50, 40], [10, 20, 30, 40, 50, 60, 70])
    '''
    # return []
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE
    #



    result = []
    if L:

        # if from_first:
            # middle,x = divmod(len(L),2)
            # middle == 1 # [10, 20, 30]
            # for index in range(middle + 1):
                # index = 0
                # index = 1
            #    result.append(L[index])
            #     if len(L) - index - 1 > middle:
            #        result.append(L[len(L) - index - 1])



        if from_first:
            for index in range(len(L)):
                a,b  = divmod(index,2)
                if b == 0:
                    result.append(L[a])
                else:
                    result.append(L[0 -(a + 1)])

        else:
            for index in range(len(L)):
                a, b = divmod(index, 2)
                if b == 0:
                    # index = 0,a = 0,b = 0
                    # index = 2 a = 1,b = 0
                    result.append(L[0 - (a + 1)])
                # index  = 1
                else:
                    # index = 1,a = 0,b = 1
                    #
                    result.append(L[a])
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
