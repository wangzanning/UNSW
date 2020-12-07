# COMP9021 19T3 - Rachid Hamadi
# Sample Exam Question 5


'''
Will be tested with year between 1913 and 2013.
You might find the reader() function of the csv module useful,
but you can also use the split() method of the str class.
'''

import csv
#import numpy as np

def f(year):
    '''
    >>> f(1914)
    In 1914, maximum inflation was: 2.0
    It was achieved in the following months: Aug
    >>> f(1922)
    In 1922, maximum inflation was: 0.6
    It was achieved in the following months: Jul, Oct, Nov, Dec
    >>> f(1995)
    In 1995, maximum inflation was: 0.4
    It was achieved in the following months: Jan, Feb
    >>> f(2013)
    In 2013, maximum inflation was: 0.82
    It was achieved in the following months: Feb
    '''
    months = 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    # Insert your code here
    a = open('cpiai.csv')
    b = csv.reader(a)
    
    b = list(b)
    print(b[:5])
    month_list = []
    for i in b:
        if str(year) in str(i[0][:4]):
            month_list.append(i)

    infl_list = []
    for i in month_list:
        infl_list.append(i[2])

    maxi = max(infl_list)

    month = []
    for i in month_list:
        if i[2] == maxi:
            month.append(i[0][5:7])
    dict1 = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',\
            '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
    output = ''

    for i in month:
        output += dict1[i] + ', '
    output = output.strip(' ')
    output = output.strip(',')
    print(f'In {year}, maximum inflation was: {maxi}')
    print(f'It was achieved in the following months: {output}')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
