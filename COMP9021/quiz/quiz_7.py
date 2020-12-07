# COMP9021 19T3 - Rachid Hamadi
# Quiz 7 *** Due Thursday Week 9
#
# Randomly generates a grid of 0s and 1s and determines
# the maximum number of "spikes" in a shape.
# A shape is made up of 1s connected horizontally or vertically (it can contain holes).
# A "spike" in a shape is a 1 that is part of this shape and "sticks out"
# (has exactly one neighbour in the shape).


from random import seed, randrange
import sys


dim = 10


def display_grid():
    for row in grid:
        print('   ', *row) 


# Returns the number of shapes we have discovered and "coloured".
# We "colour" the first shape we find by replacing all the 1s
# that make it with 2. We "colour" the second shape we find by
# replacing all the 1s that make it with 3.
num = 2
def colour_shapes():

    for i in range(10):
        for j in range(10):
            if grid[i][j] == 1:
                find_around_1(i,j)
                global num
                num += 1
            else:
                pass
    return num - 1

    # Replace pass above with your code


def find_around_1(i,j):

    if grid[i][j] == 1:
        grid[i][j] = num

        if 0 <= i+1 <= 9 and 0 <= j <= 9:
            if grid[i+1][j] == 1:
                find_around_1(i+1, j)
            else:
                pass
        if 0 <= i-1 <= 9 and 0 <= j <= 9:
            if grid[i-1][j] == 1:
                find_around_1(i-1, j)
            else:
                pass
        if 0 <= i <= 9 and 0 <= j+1 <= 9:
            if grid[i][j+1] == 1:
                find_around_1(i, j+1)
            else:
                pass
        if 0 <= i <= 9 and 0 <= j-1 <= 9:
            if grid[i][j-1] == 1:
                find_around_1(i, j-1)
            else:
                pass


def max_number_of_spikes(nb_of_shapes):
    max_spikes_list = []
    for k in range(2, nb_of_shapes+1):
        same_color_spikes = 0
        for i in range(10):
            counter_spikes = 0
            for j in range(10):
                counter_spikes = 0
                if grid[i][j] == k:
                    if 0 <= i + 1 <= 9 and 0 <= j <= 9:
                        if grid[i+1][j] == k:
                            counter_spikes += 1
                        else:
                            pass
                    if 0 <= i - 1 <= 9 and 0 <= j <= 9:
                        if grid[i - 1][j] == k:
                            counter_spikes += 1
                        else:
                            pass
                    if 0 <= i <= 9 and 0 <= j + 1 <= 9:
                        if grid[i][j + 1] == k:
                            counter_spikes += 1
                        else:
                            pass
                    if 0 <= i <= 9 and 0 <= j - 1 <= 9:
                        if grid[i][j - 1] == k:
                            counter_spikes += 1
                        else:
                            pass
                    if counter_spikes == 1:
                        same_color_spikes += 1

        max_spikes_list.append(same_color_spikes)
    maximum_spikes = max(max_spikes_list)
    return maximum_spikes
    # Replace pass above with your code


# Possibly define other functions here    


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
nb_of_shapes = colour_shapes()
print('The maximum number of spikes of some shape is:',
      max_number_of_spikes(nb_of_shapes)
     )
