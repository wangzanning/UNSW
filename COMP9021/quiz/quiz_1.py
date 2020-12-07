# COMP9021 19T3 - Rachid Hamadi
# Quiz 1 *** Due Thursday Week 2


import sys
from random import seed, randrange

try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 2, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)

nonkeys = []
mapping_as_a_list = []
one_to_one_part_of_mapping = {}

# INSERT YOUR CODE HERE
# number of element
print('\nThe mapping is  so-called "keys" make up a set whose number of element is', str(len(mapping)) +'.')

# nonkeys
key = list(mapping.keys())
value = list(mapping.values())
nonkeys = list(range(1, upper_bound))
for i in key:
    if i in nonkeys:
        nonkeys.remove(i)
print('\nThe list of integers between 1 and', upper_bound - 1, 'that are not keys of the mapping is:')
print('  ', nonkeys)

# mapping_as_a_list
Find_mapping = list(range(0, upper_bound))
for k in Find_mapping:
    if k in key:
        mapping_as_a_list.append(mapping.get(k))
    else:
        mapping_as_a_list.append(None)

print('\nRepresented as a list, the mapping is:v')
print('  ', mapping_as_a_list)

# onr-to-one mapping
# Recreating the dictionary, inserting keys from smallest to largest,
# to make sure the dictionary is printed out with keys from smallest to largest.

new_list = mapping_as_a_list.copy()
new_value_list = list()

for k in value:
    if value.count(k) == 1:
        new_value_list.append(k)

for k in new_value_list:
    new_key = key[value.index(k)]
    one_to_one_part_of_mapping[new_key] = k



one_to_one_part_of_mapping = {key: one_to_one_part_of_mapping[key]
                              for key in sorted(one_to_one_part_of_mapping)
                              }

print('\nThe one-to-one part of the mapping is:')
print('  ', one_to_one_part_of_mapping)
