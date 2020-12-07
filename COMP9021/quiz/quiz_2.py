# COMP9021 19T3 - Rachid Hamadi
# Quiz 2 *** Due Thursday Week 3


import sys
from random import seed, randrange
from pprint import pprint

try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 8, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)
# sorted() can take as argument a list, a dictionary, a set...
keys = sorted(mapping.keys())
print('\nThe keys are, from smallest to largest: ')
print('  ', keys)

cycles = []
reversed_dict_per_length = {}

# INSERT YOUR CODE HERE
values_list = list(mapping.values())
# find the cycles
# get and pop the items which value = key
equal_cycles = list()
new_mapping = mapping.copy()
for k in mapping:
    if k == mapping.get(k):
        new_mapping.pop(k)
        equal_cycles.append([k])

new_key = list(new_mapping.keys())
new_value = list(new_mapping.values())

# get the list by key (one by one)
for k in new_key:
    cycles = []  # clean the cycles before try new key
    test_key = k
    cycles.append(k)
    counter = 1
    for counter in range(1, len(new_key) + 1):  # get list with value = mapping[key]
        temp_value = mapping.get(test_key)
        cycles.append(temp_value)
        if temp_value is None:  # stop the list ,and pop the number value we get < key
            cycles.pop()
            break
        if temp_value == k:
            cycles.pop()
            break
        test_key = temp_value
    # if the last number in the list = test number then break the cycles
    try:
        if mapping[cycles[-1]] == k:

            break
        else:
            cycles.clear()
    except:
        KeyError

equal_cycles.append(cycles)  # append two list together then sorted the list


if [] in equal_cycles:
    equal_cycles.remove([])
cycles = sorted(equal_cycles)


# triply ordered
opposite_dict = dict()

for key, value in mapping.items():  # create the opposite dict
    opposite_dict_key = list(opposite_dict.keys())
    if value in opposite_dict_key:
        opposite_dict[value].append(key)
    else:
        opposite_dict[value] = [key]
value_list = []
temp_dict = {}
k_dict = {}
opposite_dict_value = opposite_dict.values()
for value in opposite_dict_value:  # get the length of value in opposite dict
    length_value = len(value)
    value_list.append(length_value)

for length in set(value_list):  # cycle in different length of opposite dict
    k_dict[length] = {}
    for key, value in opposite_dict.items():
        if len(value) == length:
            k_dict[length][key] = value  # print the dict with length
            reversed_dict_per_length = k_dict

print('\nProperly ordered, the cycles given by the mapping are: ')
print('  ', cycles)
print('\nThe (triply ordered) reversed dictionary per lengths is: ')
pprint(reversed_dict_per_length)
