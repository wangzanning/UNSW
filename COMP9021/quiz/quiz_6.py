# COMP9021 19T3 - Rachid Hamadi
# Quiz 6 *** Due Thursday Week 8
#
# Randomly fills an array of size 10x10 with 0s and 1s, and outputs the size of
# the largest parallelogram with horizontal sides.
# A parallelogram consists of a line with at least 2 consecutive 1s,
# with below at least one line with the same number of consecutive 1s,
# all those lines being aligned vertically in which case the parallelogram
# is actually a rectangle, e.g.
#      111
#      111
#      111
#      111
# or consecutive lines move to the left by one position, e.g.
#      111
#     111
#    111
#   111
# or consecutive lines move to the right by one position, e.g.
#      111
#       111
#        111
#         111


from random import seed, randrange
import sys


dim = 10


def display_grid():
    for row in grid:
        print('   ', *row) 


def size_of_largest_parallelogram():
    output_list = []
    #find to the down
    for i in range(10):
        i_posit = i
        for j in range(10):
            j_posit = j
            counter_1_length = 0
            for length in range(2, 11-j):
                counter_1_length = 0
                counter_1_height = 0

                while counter_1_length < length:
                    if grid[i][j] == 1:
                        counter_1_length += 1
                        j += 1
                        if j == 10:
                            break
                    else:
                        break
                j = j_posit
                if counter_1_length != length:
                    break
                while True:
                    temp_length = 0
                    for k in range(0, counter_1_length):
                        if grid[i][j + k] == 1:
                            temp_length += 1
                        else:
                            break
                    if temp_length == length:
                        counter_1_height += 1
                        i += 1
                        if i == 10:
                            break
                    else:
                        break
                i = i_posit
                if counter_1_height == 1:
                    pass
                else:
                    output = counter_1_length * counter_1_height
                    output_list.append(output)
    #find to the right
    for i in range(10):
        i_posit = i
        for j in range(10):
            j_posit = j
            counter_1_length = 0
            for length in range(2, 11-j):
                counter_1_length = 0
                counter_1_height = 0

                while counter_1_length < length:
                    if grid[i][j] == 1:
                        counter_1_length += 1
                        j += 1
                        if j == 10:
                            break
                    else:
                        break
                j = j_posit
                if counter_1_length != length:
                    break
                while True:
                    temp_length = 0
                    for k in range(0, counter_1_length):
                        if j + counter_1_length == 10:
                            break
                        if grid[i][j + k] == 1:
                            temp_length += 1
                        else:
                            break
                    if temp_length == length:
                        counter_1_height += 1
                        i += 1
                        j += 1
                        if i == 10:
                            break
                        if j == 10:
                            break
                    else:
                        break
                i = i_posit
                if counter_1_height == 1 or counter_1_height == 0:
                    pass
                else:
                    output = counter_1_length * counter_1_height
                    output_list.append(output)

    #find to the left
    for i in range(10):
        i_posit = i
        for j in range(10):
            j_posit = j
            counter_1_length = 0
            if grid[i][j] == 0:
                continue
            for length in range(2, 10):
                counter_1_length = 0
                counter_1_height = 0

                while counter_1_length < length:
                    if grid[i][j] == 1:
                        counter_1_length += 1
                        j += 1
                        if j == 10:
                            break
                    else:
                        break
                j = j_posit
                if counter_1_length != length:
                    break
                while True:
                    temp_length = 0
                    for k in range(0, counter_1_length):
                        if j + k == 10:
                            break
                        if grid[i][j + k] == 1:
                            temp_length += 1
                        else:
                            break
                    if temp_length == length:
                        counter_1_height += 1
                        i += 1
                        j -= 1
                        if i == 10:
                            break
                        if j == -1:
                            break
                    else:
                        break
                i = i_posit
                j = j_posit

                if counter_1_height == 1 or counter_1_height == 0:
                    pass
                else:
                    output = counter_1_length * counter_1_height
                    output_list.append(output)


    if output_list == []:
        return False
    else:
        final_output = max(output_list)
        return final_output

    # REPLACE PASS ABOVE WITH YOUR CODE


# POSSIBLY DEFINE OTHER FUNCTIONS


try:
    
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
size = size_of_largest_parallelogram()
if size:
    print('The largest parallelogram with horizontal sides '
          f'has a size of {size}.'
         )
else:
    print('There is no parallelogram with horizontal sides.')
