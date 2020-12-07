from random import seed, randint
import sys

def f(arg_for_seed, nb_of_elements, max_element):
    '''
    >>> f(0, 0, 10)
    Here is L: []
    >>> f(0, 1, 10)
    Here is L: [6]
    1 element starts with 6
    >>> f(0, 2, 10)
    Here is L: [6, 6]
    2 elements start with 6
    >>> f(1, 2, 100)
    Here is L: [17, 72]
    1 element starts with 1
    1 element starts with 7
    >>> f(2, 3, 1000)
    Here is L: [978, 883, 970]
    1 element starts with 8
    2 elements start with 9
    >>> f(8, 6, 1000)
    Here is L: [232, 379, 985, 384, 129, 197]
    2 elements start with 1
    1 element starts with 2
    2 elements start with 3
    1 element starts with 9
    >>> f(20, 8, 10000)
    Here is L: [2477, 4257, 1663, 5364, 9387, 2775, 442, 6742]
    1 element starts with 1
    2 elements start with 2
    2 elements start with 4
    1 element starts with 5
    1 element starts with 6
    1 element starts with 9
    '''
    seed(arg_for_seed)
    L = [randint(0,max_element) for _ in range(nb_of_elements)]
    print ('Here is L:',L)

    first_list =[]
    for i in L:
        i = str(i)
        first = i[0]
        first_list.append(i[0])
    if '1' in first_list:
        counter = first_list.count('1')
        if counter ==1:
            print(f'{counter} element starts with 1')
        else:
            print(f'{counter} elements start with 1')

        
    if '2' in first_list:
        counter = first_list.count('2')
        if counter ==1:
            print(f'{counter} element starts with 2')
        else:
            print(f'{counter} elements start with 2')
    if '3' in first_list:
        counter = first_list.count('3')
        if counter ==1:
            print(f'{counter} element starts with 3')
        else:
            print(f'{counter} elements start with 3')
    if '4' in first_list:
        counter = first_list.count('4')
        if counter ==1:
            print(f'{counter} element starts with 4')
        else:
            print(f'{counter} elements start with 4')
    if '5' in first_list:
        counter = first_list.count('5')
        if counter ==1:
            print(f'{counter} element starts with 5')
        else:
            print(f'{counter} elements start with 5')
    if '6' in first_list:
        counter = first_list.count('6')
        if counter ==1:
            print(f'{counter} element starts with 6')
        else:
            print(f'{counter} elements start with 6')
    if '7' in first_list:
        counter = first_list.count('7')
        if counter ==1:
            print(f'{counter} element starts with 7')
        else:
            print(f'{counter} elements start with 7')
    if '8' in first_list:
        counter = first_list.count('8')
        if counter ==1:
            print(f'{counter} element starts with 8')
        else:

            print(f'{counter} elements start with 8')
    if '9' in first_list:
        counter = first_list.count('9')
        if counter ==1:
            print(f'{counter} element starts with 9')
        else:
            print(f'{counter} elements start with 9')



if __name__ == '__main__':
    import doctest
    doctest.testmod()
