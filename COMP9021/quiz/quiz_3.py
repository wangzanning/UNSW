# COMP9021 19T3 - Rachid Hamadi
# Quiz 3 *** Due Thursday Week 4


# Reading the number written in base 8 from right to left,
# keeping the leading 0's, if any:
# 0: move N     1: move NE    2: move E     3: move SE
# 4: move S     5: move SW    6: move W     7: move NW
#
# We start from a position that is the unique position
# where the switch is on.
#
# Moving to a position switches on to off, off to on there.

import sys

on = '\u26aa'
off = '\u26ab'
code = input('Enter a non-strictly negative integer: ').strip()
try:
    if code[0] == '-':
        raise ValueError
    int(code)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
nb_of_leading_zeroes = 0
print(type(code))
for i in range(len(code) - 1):
    if code[i] == '0':
        nb_of_leading_zeroes += 1
    else:
        break
print("Keeping leading 0's, if any, in base 8,", code, 'reads as',
      '0' * nb_of_leading_zeroes + f'{int(code):o}.'
      )
print()

# INSERT YOUR CODE HERE
number_8_base = '0' * nb_of_leading_zeroes + f'{int(code):o}'
number_8_base = list(number_8_base)
number_8_base.reverse()
how_to_move = {'0': [0, 1], '1': [1, 1], '2': [1, 0], '3': [1, -1], '4': [0, -1], '5': [-1, -1], '6': [-1, 0], '7': [-1, 1]}
list_pass_by = [[0, 0]]
pass_point = [0, 0]


# for list add
def list_add(a, b):
    result = []
    for i in range(2):
        result.append(a[i] + b[i])
    return result


for i in number_8_base:
    pass_point = list_add(pass_point, how_to_move.get(i))
    list_pass_by.append(pass_point)
# get the range of x and y
x_list = []
y_list = []
for i in list_pass_by:
    x_list.append(i[0])
for i in list_pass_by:
    y_list.append(i[1])
range_x = max(x_list) - min(x_list) + 1
range_y = max(y_list) - min(y_list) + 1
# delete the point pass by 2 times or 4,6...
for i in list_pass_by:
    if list_pass_by.count(i) % 2 == 0:
        while i in list_pass_by:
            list_pass_by.remove(i)
# cut the black edge
new_y_list_max = max(y_list)
new_y_list_min = min(y_list)
new_x_list_max = max(x_list)
new_x_list_min = min(x_list)
counter = 0
for y in range(max(y_list), min(y_list) - 1, -1):  # x left edge
    if [min(x_list),y] not in list_pass_by:
        counter += 1
if counter == range_y:
    new_x_list_min = new_x_list_min + 1
counter = 0
for y in range(max(y_list), min(y_list) - 1, -1):  # x right edge
    if [max(x_list),y] not in list_pass_by:
        counter += 1
if counter == range_y:
    new_x_list_max = new_x_list_max - 1
counter = 0
for x in range(min(x_list), max(x_list) + 1):  # y down edge
    if [x,min(y_list)] not in list_pass_by:
        counter += 1
if counter == range_x:
    new_y_list_min = new_y_list_min + 1
counter = 0
for x in range(min(x_list), max(x_list) + 1):  # y up edge
    if [x,max(y_list)] not in list_pass_by:
        counter += 1
if counter == range_x:
    new_y_list_max = new_y_list_max - 1
# just print
for y in range(new_y_list_max, new_y_list_min - 1, -1):
    for x in range(new_x_list_min, new_x_list_max + 1):
        if [x, y] in list_pass_by:
            print(on,end='')
        else:
            print(off,end='')
    print('')


