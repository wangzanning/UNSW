# COMP9021 19T3 - Rachid Hamadi
# Quiz 5 *** Due Thursday Week 7
#
# Implements a function that, based on the encoding of
# a single strictly positive integer that in base 2,
# reads as b_1 ... b_n, as b_1b_1 ... b_nb_n, encodes
# a sequence of strictly positive integers N_1 ... N_k
# with k >= 1 as N_1* 0 ... 0 N_k* where for all 0 < i <= k,
# N_i* is the encoding of N_i.
#
# Implements a function to decode a positive integer N
# into a sequence of (one or more) strictly positive
# integers according to the previous encoding scheme,
# or return None in case N does not encode such a sequence.


import sys


def encode(list_of_integers):
    list_2_byte = []
    for i in list_of_integers:
        temp_2 = bin(int(i))[2:]
        list_2_byte.append(temp_2)
    double_list = []
    for i in list_2_byte:
        i = list(i)
        temp_i = ''
        for k in i:
            temp_i += k+k
        double_list.append(temp_i)
    new_value_2_byte = ''
    for i in double_list:
        new_value_2_byte += '0'+ i
    new_value_2_byte = str(new_value_2_byte)[1:]
    outputvalue_10_byte = int(new_value_2_byte, 2)
    return outputvalue_10_byte

    # REPLACE pass ABOVE WITH YOUR CODE    


def decode(integer):
    integer_2_byte = bin(int(integer))[2:]
    integer_2_byte = list(integer_2_byte)
    expected_result_2_byte = ''
    while len(integer_2_byte) > 0:
        if len(integer_2_byte) == 1:
            return None
        a = integer_2_byte[0]
        b = integer_2_byte[1]
        if a == b == '0':
            expected_result_2_byte += '0'
            integer_2_byte.remove(a)
            integer_2_byte.remove(b)
        elif a == b == '1':
            expected_result_2_byte += '1'
            integer_2_byte.remove(a)
            integer_2_byte.remove(b)
        elif a == '0' and b == '1':
            expected_result_2_byte += ','
            integer_2_byte.remove(a)
        elif a == '1' and b == '0':
            return None

    expected_result_2_list = expected_result_2_byte.split(',')
    output_10_byte = []
    for i in expected_result_2_list:
        temp_output = int(i, 2)
        output_10_byte.append(temp_output)
    return output_10_byte
    # REPLACE pass ABOVE WITH YOUR CODE


# We assume that user input is valid. No need to check
# for validity, nor to take action in case it is invalid.
print('Input either a strictly positive integer')
the_input = eval(input('or a nonempty list of strictly positive integers: '))
if type(the_input) is int:
    print('  In base 2,', the_input, 'reads as', bin(the_input)[2 :])
    decoding = decode(the_input)
    if decoding is None:
        print('Incorrect encoding!')
    else:
        print('  It encodes: ', decode(the_input))
else:
    print('  In base 2,', the_input, 'reads as',
          f'[{", ".join(bin(e)[2: ] for e in the_input)}]'
         )
    print('  It is encoded by', encode(the_input))
