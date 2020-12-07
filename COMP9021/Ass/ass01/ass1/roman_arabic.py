import sys
# First kind of input


def alabo_2_roman(input_alabo):
    ala_rom_dict = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC',
                    50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
    ala_list = list(ala_rom_dict.keys())
    result_rom = ''
    input_alabo = int(input_alabo)
    for i in range(len(ala_list)):
        while input_alabo >= ala_list[i]:
            input_alabo -= ala_list[i]
            result_rom += ala_rom_dict.get(ala_list[i])
    return result_rom


def roman_2_alabo(input_roman):
    rom_ala_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if input_roman == '0':
        return 0
    else:
        result_ala = 0
        for i in range(0,len(input_roman)):
            if i == 0 or rom_ala_dict.get(input_roman[i]) <= rom_ala_dict.get(input_roman[i-1]):
                result_ala += rom_ala_dict.get(input_roman[i])
            else:
                result_ala += rom_ala_dict.get(input_roman[i]) - 2*rom_ala_dict.get(input_roman[i-1])
    return result_ala


user_input_begin = input('How can I help you?').strip()
user_input_begin_list = user_input_begin.split(' ')
length_input = len(user_input_begin_list)
if user_input_begin_list[0] != 'Please' or user_input_begin_list.count('Please') >1:
    print(' I don\'t get what you want, sorry mate!')
    sys.exit()

if length_input < 3 or length_input >5 or user_input_begin_list[1] != 'convert':
    print(' I don\'t get what you want, sorry mate!')
    sys.exit()
if length_input == 5 and user_input_begin_list[-2] != 'using':
    print(' I don\'t get what you want, sorry mate!')
    sys.exit()
if ('using' not in user_input_begin_list and 'minimally' not in user_input_begin_list) \
        and user_input_begin_list[-1] != 'convert' and length_input != 3:
    print(' I don\'t get what you want, sorry mate!')
    sys.exit()
if length_input == 4 and user_input_begin_list[-1] != 'minimally':
    print(' I don\'t get what you want, sorry mate!')
    sys.exit()
if ('using' in user_input_begin and 'convert' in user_input_begin) and '_' in user_input_begin_list:
    print(' Hey, ask me something that\'s not impossible to do!')
    sys.exit()

user_input = user_input_begin[15:]
if user_input.isdigit() and ' ' not in user_input:
    if user_input[0] == '0' or int(user_input) >= 4000:
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()

    if int(user_input) >= 0 and int(user_input) < 4000:
        output_rom = alabo_2_roman(user_input)
        print(' Sure! It is', output_rom)
        sys.exit()
if user_input.isalpha() and 'using' not in user_input and 'minimally' not in user_input:
    rom_chr_list = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
    output_ala = 0
    counter = 0
    for i in list(user_input):
        if i in rom_chr_list:
            counter += 1
    if len(user_input) == counter:
        output_ala = roman_2_alabo(user_input)
    else:
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    if alabo_2_roman(output_ala) == user_input:
        print(' Sure! It is', output_ala)
        sys.exit()
    else:
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()


# second of input
convert_index = user_input_begin.index('convert')
if 'using' in user_input_begin:
    using_index = user_input_begin.index('using')
    using_value = user_input_begin[using_index + 5:].strip()
    convert_value = user_input_begin[convert_index + 7:using_index].strip()


def gener_rom_2_ala(convert_value,using_value):
    using_value = list(reversed(using_value))
    gener_rom_ala_dict = {}
    k = 1
    for i in range(len(using_value)):
        if i == 0:
            gener_rom_ala_dict[using_value[0]] = 1
        else:
            if i % 2 == 1:
                k = k * 5
                gener_rom_ala_dict[using_value[i]] = k
            if i % 2 == 0:
                k = k * 2
                gener_rom_ala_dict[using_value[i]] = k
    if convert_value == '0':
        return 0
    else:
        result_ala_gene = 0
        for i in range(0, len(convert_value)):
            if i == 0 or gener_rom_ala_dict.get(convert_value[i]) <= gener_rom_ala_dict.get(convert_value[i-1]):
                result_ala_gene += gener_rom_ala_dict.get(convert_value[i])
            else:
                result_ala_gene += gener_rom_ala_dict.get(convert_value[i]) - \
                                   2 * gener_rom_ala_dict.get(convert_value[i-1])
    return result_ala_gene


def gener_ala_2_rom(convert_value, using_value):
    using_value = list(reversed(using_value))
    ala_value_list = []
    gener_roma_list = []
    k = (len(using_value) * 2 - 1) // 4
    l = (len(using_value) * 2 - 1) % 4
    for i in range(k):
        four_list = [1*pow(10, i), 4*pow(10, i), 5*pow(10, i), 9*pow(10, i)]
        ala_value_list += four_list
    if l == 1:
        ala_value_list += [1*pow(10,k)]
    else:
        ala_value_list += [1*pow(10, k), 4*pow(10, k), 5*pow(10, k)]
    for i in range(k):
        f = [using_value[2*i], using_value[2*i]+using_value[2*i+1],
             using_value[2*i+1], using_value[2*i]+using_value[2*i+2]]
        gener_roma_list += f
    if l == 1:
        gener_roma_list += [using_value[2*k]]
    else:
        gener_roma_list += [using_value[2*k], using_value[2*k]+using_value[2*k+1],
                            using_value[2*k+1]]
    ala_value_list = reversed(ala_value_list)
    gener_roma_list = reversed(gener_roma_list)
    gener_ala_rom_dict = dict(zip(ala_value_list, gener_roma_list))
    gener_ala_rom_dict_keys = list(gener_ala_rom_dict.keys())
    result_rom_gener = ''
    convert_value = int(convert_value)
    for i in range(len(gener_ala_rom_dict_keys)):
        while convert_value >= gener_ala_rom_dict_keys[i]:
            convert_value -= gener_ala_rom_dict_keys[i]
            result_rom_gener += gener_ala_rom_dict.get(gener_ala_rom_dict_keys[i])
    return result_rom_gener
#q2 ala 2 rom
if 'using' in user_input_begin and convert_value.isdigit():
    if not using_value.isalpha() or len(set(using_value)) != len(using_value):
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    if convert_value[0] == '0':
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    else:
        q2_output_roman = gener_ala_2_rom(convert_value, using_value)
        q2_output_roman_list = list(q2_output_roman)
        for i in list(q2_output_roman_list):
            if q2_output_roman_list.count(i) == 4 and i + i + i + i in q2_output_roman:
                print(' Hey, ask me something that\'s not impossible to do!')
                sys.exit()
        print(' Sure! It is',q2_output_roman)
        sys.exit()
#q2 rom 2 ala
if 'using' in user_input_begin and convert_value.isalpha():
    try:
        q2_output_ala = gener_rom_2_ala(convert_value, using_value)
    except TypeError or ValueError or IndexError:
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    if q2_output_ala < 4000 and len(alabo_2_roman(q2_output_ala)) != len(convert_value):
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    if '_' in using_value or '_' in convert_value:
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    if not using_value.isalpha() or len(set(using_value)) != len(using_value):
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    if gener_ala_2_rom(q2_output_ala,using_value) == convert_value:
        print(' Sure! It is',q2_output_ala)
        sys.exit()
    else:
        print(' Hey, ask me something that\'s not impossible to do!')
        sys.exit()
# third of input
mini_index = user_input_begin.index('minimally')
mini_value_input = user_input_begin[convert_index + 7:mini_index].strip()


def convert_minimally(mini_value_input):
    reversed_value = mini_value_input[::-1]
    mini_value = list(reversed(mini_value_input))
    expected_result_without_value = []
    mini_value_remove_dupl = sorted(set(mini_value), key=mini_value.index)
    a = mini_value_remove_dupl[0]

    if len(mini_value_remove_dupl) > 1:
        b = mini_value_remove_dupl[1]
    if len(mini_value_remove_dupl) > 2:
        c = mini_value_remove_dupl[2]
        k_temp =a+b+mini_value.count(c)*c
    if len(mini_value_remove_dupl) > 3:
        d = mini_value_remove_dupl[3]
    if len(mini_value_remove_dupl) > 2:
        if mini_value.count(a) == 1 and mini_value.count(b) == 1 and mini_value.count(c)\
                >=2 and k_temp in reversed_value:
            expected_result_without_value += [b, a]
            mini_value_remove_dupl.remove(a)
            mini_value_remove_dupl.remove(b)

    while len(mini_value_remove_dupl) > 0:
        a = mini_value_remove_dupl[0]
        count_a = mini_value.count(a)
        if len(mini_value_remove_dupl) > 1:
            b = mini_value_remove_dupl[1]
            count_b = mini_value.count(b)
        if len(mini_value_remove_dupl) > 2:
            c = mini_value_remove_dupl[2]
            count_c = mini_value.count(c)
        if len(mini_value_remove_dupl) > 3:
            d = mini_value_remove_dupl[3]
            count_d = mini_value.count(d)
        if len(mini_value_remove_dupl) == 1:
            expected_result_without_value += [a]
            mini_value_remove_dupl.remove(a)
        elif len(mini_value_remove_dupl) == 2:
            if count_a == 1 and count_b == 1:
                expected_result_without_value += [b,a]
                mini_value_remove_dupl.remove(a)
                mini_value_remove_dupl.remove(b)
            else:
                expected_result_without_value += [a,b]
                mini_value_remove_dupl.remove(a)
                mini_value_remove_dupl.remove(b)
        elif count_a == 1 and count_b == 1 and count_c >= 2 and a+b+count_c*c in reversed_value:
            expected_result_without_value += [a,b]
            mini_value_remove_dupl.remove(a)
            mini_value_remove_dupl.remove(b)
        elif ((count_a > 1 and count_b == 1 and count_c == 1) or (count_a ==1 and count_b > 1 and count_c == 1) or\
                (count_a == 1 and count_b == 1 and count_c > 1)) and\
                a*count_a + b*count_b + c*count_c in reversed_value:
            expected_result_without_value += [a,b]
            mini_value_remove_dupl.remove(a)
            mini_value_remove_dupl.remove(b)
        elif count_a > 1 and count_b == 1 and count_c == 1 and\
                (a+b+a*(count_a-1)+c in reversed_value or a*(count_a-1)+b+a+c in reversed_value):
            expected_result_without_value += [b,a,c]
            mini_value_remove_dupl.remove(a)
            mini_value_remove_dupl.remove(b)
            mini_value_remove_dupl.remove(c)
        elif count_a > 1 and count_b > 1 and count_c > 1 and a*count_a + b*count_b + c*count_c in reversed_value:
            expected_result_without_value += [a,b]
            mini_value_remove_dupl.remove(a)
            mini_value_remove_dupl.remove(b)
        elif ((count_a == 1 and count_b > 1 and count_c > 1) or (count_a > 1 and count_b == 1 and count_c > 1) or
              (count_a > 1 and count_b > 1 and count_c == 1)) and (a*count_a+b*count_b+c*count_c in reversed_value or\
                                                                   a*count_a+b*count_b+c in reversed_value):
            expected_result_without_value += [a,b]
            mini_value_remove_dupl.remove(a)
            mini_value_remove_dupl.remove(b)
        elif count_a > 1 and count_b == 1 and count_c > 1 and a+b+c+a in reversed_value:
            expected_result_without_value += [b,a,c]
            mini_value_remove_dupl.remove(a)
            mini_value_remove_dupl.remove(b)
            mini_value_remove_dupl.remove(c)
        elif count_a == count_b == count_c == count_d == 1 and a+b+c+d in reversed_value:
            expected_result_without_value += [b,a,d,c]
            mini_value_remove_dupl.remove(a)
            mini_value_remove_dupl.remove(b)
            mini_value_remove_dupl.remove(c)
            mini_value_remove_dupl.remove(d)
        elif ((count_a > 1 and count_b == 2 and count_c == 1) or (count_a == 1 and count_b > 2 and count_c == 1))and\
            ((a*count_a+b+c+b in reversed_value)or(a+b+c+b*count_b in reversed_value)):
            expected_result_without_value += [a,c,b]
            mini_value_remove_dupl.remove(a)
            mini_value_remove_dupl.remove(b)
            mini_value_remove_dupl.remove(c)
        else:
            return 'nothing'

    length = 1
    expected_result_with_value = []
    expected_result_with_value += [expected_result_without_value[0]]
    expected_result_with_value[0] = expected_result_without_value[0]
    for i in range(1, len(expected_result_without_value)):
        if i < len(expected_result_without_value) - 1:
            t = expected_result_without_value[i + 1]
        k = expected_result_without_value[i - 1]
        p = expected_result_without_value[i]
        if reversed_value.count(p) > 1:
            if length % 2 == 1:
                expected_result_with_value += '_' + p
                length += 2
            else:
                if p + k + p in reversed_value:
                    expected_result_with_value += '_' + p
                    length += 2
                else:
                    expected_result_with_value += p
                    length += 1
        if reversed_value.count(p) == 1:
            if i < len(expected_result_without_value) - 1:
                if t + p + t in reversed_value:
                    expected_result_with_value += '_' + p
                    length += 2
                else:
                    expected_result_with_value += p
                    length += 1
            else:
                expected_result_with_value += p
                length += 1

    output_using_value = ''
    for i in expected_result_with_value:
        output_using_value += i
    output_using_value = output_using_value[::-1]
    strange_roman_ala_dict = {}
    begin_value = 1
    for i in range(len(expected_result_with_value)):
        if i == 0:
            strange_roman_ala_dict[expected_result_with_value[i]] = begin_value
        else:
            if i % 2 == 1:
                begin_value = begin_value * 5
                if expected_result_with_value[i] != '_':
                    strange_roman_ala_dict[expected_result_with_value[i]] = begin_value
            if i % 2 == 0:
                begin_value = begin_value * 2
                if expected_result_with_value[i] != '_':
                    strange_roman_ala_dict[expected_result_with_value[i]] = begin_value
                else:
                    pass

    if mini_value_input == '0':
        pass
    else:
        output_result_third_ala = 0
        for i in range(0, len(mini_value_input)):
            if i == 0 or strange_roman_ala_dict.get(mini_value_input[i])\
                    <= strange_roman_ala_dict.get(mini_value_input[i-1]):
                output_result_third_ala += strange_roman_ala_dict.get(mini_value_input[i])
            else:
                y1 = strange_roman_ala_dict.get(mini_value_input[i])
                y2 = strange_roman_ala_dict.get(mini_value_input[i-1])
                output_result_third_ala += y1 - 2 * y2
    return [output_result_third_ala,output_using_value]
try:
    output_third_value = convert_minimally(mini_value_input)[0]
    output_third_using = convert_minimally(mini_value_input)[1]
except UnboundLocalError or IndexError:
    print(' Hey, ask me something that\'s not impossible to do!')
    sys.exit()
if convert_minimally(mini_value_input) == 'nothing':
    print(' Hey, ask me something that\'s not impossible to do!')
    sys.exit()
if not mini_value_input.isalpha():
    print(' Hey, ask me something that\'s not impossible to do!')
    sys.exit()
if output_third_value < 4000 and len(alabo_2_roman(output_third_value)) != len(mini_value_input):
    print(' Hey, ask me something that\'s not impossible to do!')
    sys.exit()

print(f' Sure! It is {output_third_value} using {output_third_using}')
sys.exit()



