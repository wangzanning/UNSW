# COMP9021 19T3 - Rachid Hamadi
# Quiz 4 *** Due Thursday Week 5
#
# Prompts the user for an arity (a natural number) n and a word.
# Call symbol a word consisting of nothing but alphabetic characters
# and underscores.
# Checks that the word is valid, in that it satisfies the following
# inductive definition:
# - a symbol, with spaces allowed at both ends, is a valid word;
# - a word of the form s(w_1,...,w_n) with s denoting a symbol and
#   w_1, ..., w_n denoting valid words, with spaces allowed at both ends
#   and around parentheses and commas, is a valid word.
import sys


def check_word_valid(test_words):  # check words if satisfy definition
    a = list(chr(i) for i in range(65, 91))  # upper alpha
    b = list(chr(i) for i in range(97, 123))  # lower alpha
    c = ["_"]
    valid_range = a+b+c  # alphabetic characters and underscores
    test_words_length1 = list(test_words)  # check one by one if it was not single character
    for word_valid in test_words_length1:
        if word_valid not in valid_range:
            return False
    return True


def is_valid(word, arity):
    line = word
    line = line.replace(" ", "")  # remove " ", very important to check valid
    if arity == 0:
        return check_word_valid(line)
    else:
        if line.find(')') == -1 or line.find('(') == -1:  # check the word if use other bracket(like[,{)
            return False
        if line.count('(') == line.count(')'):  # make sure ( = )
            pass
        else:
            return False
        while line.find(')') != -1:  # keep find ")" until it disappear
            right_parentheses_index = line.find(')')  # slice without right parentheses
            test_list_valid = line[:right_parentheses_index]
            left_parentheses_index = test_list_valid.rfind('(')  # slice without left
            test_list_valid = test_list_valid[left_parentheses_index + 1:right_parentheses_index]
            elements = test_list_valid.split(',')  # split word to check

            if '' in elements:  # if " " in elements, return false dirctly
               return False
            for i in elements:  # check value valid
                if check_word_valid(i) == False:
                    return False
            if len(elements) != arity:
                return False
            #  slice with the left and right parentheses and joint it
            line = line[:left_parentheses_index] + line[right_parentheses_index + 1:]
        if ',' in line :
            return False

    return True
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE

try:
    arity = int(input('Input an arity : '))
    if arity < 0:
        raise ValueError
except ValueError:
    print('Incorrect arity, giving up...')
    sys.exit()
word = input('Input a word: ')
if is_valid(word, arity):
    print('The word is valid.')
else:
    print('The word is invalid.')

