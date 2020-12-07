
dictionary_file = 'dictionary.txt'

def number_of_words_in_dictionary(word_1, word_2):
    '''
    "dictionary.txt" is stored in the working directory.

    >>> number_of_words_in_dictionary('company', 'company')
    Could not find company in dictionary.
    >>> number_of_words_in_dictionary('company', 'comparison')
    Could not find at least one of company and comparison in dictionary.
    >>> number_of_words_in_dictionary('COMPANY', 'comparison')
    Could not find at least one of COMPANY and comparison in dictionary.
    >>> number_of_words_in_dictionary('company', 'COMPARISON')
    Could not find at least one of company and COMPARISON in dictionary.
    >>> number_of_words_in_dictionary('COMPANY', 'COMPANY')
    COMPANY is in dictionary.
    >>> number_of_words_in_dictionary('COMPARISON', 'COMPARISON')
    COMPARISON is in dictionary.
    >>> number_of_words_in_dictionary('COMPANY', 'COMPARISON')
    Found 14 words between COMPANY and COMPARISON in dictionary.
    >>> number_of_words_in_dictionary('COMPARISON', 'COMPANY')
    Found 14 words between COMPARISON and COMPANY in dictionary.
    >>> number_of_words_in_dictionary('CONSCIOUS', 'CONSCIOUSLY')
    Found 2 words between CONSCIOUS and CONSCIOUSLY in dictionary.
    >>> number_of_words_in_dictionary('CONSCIOUS', 'CONSCIENTIOUS')
    Found 3 words between CONSCIOUS and CONSCIENTIOUS in dictionary.
    '''
    # print()
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE

    counter = 0
    if word_1 == word_2:
        if not word_1.isupper():
            counter+=1
    else:
        if not word_1.isupper():
            counter +=1
        if not word_2.isupper():
            counter +=1
    if counter ==1 and word_1 == word_2:
        print(f'Could not find {word_1} in dictionary.')
        
    if counter >= 1 and word_1 != word_2:
        print(f'Could not find at least one of {word_1} and {word_2} in dictionary.')
    if counter == 0:
        opendict = list(open('dictionary.txt'))
        opendict = [i[:-1] for i in opendict]
        index1 = opendict.index(word_1)
        index2 = opendict.index(word_2)
        
        if index2 > index1:
            number = index2 - index1 +1
        elif index2 < index1:
            number = index1 - index2 +1
        else:
            number = 0
        if number == 0:
            print(f'{word_1} is in dictionary.')
        else:
            print(f'Found {number} words between {word_1} and {word_2} in dictionary.')
            
    
    
    
if __name__ == '__main__':     
    import doctest
    doctest.testmod()
