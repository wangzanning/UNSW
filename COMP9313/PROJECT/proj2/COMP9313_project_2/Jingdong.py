depth = int(input())
dict_tri = {}
k = 0
total = 0


while k <= depth - 1:
    dict_tri[k] = [int(i) for i in input().split()]
    k = k + 1


def check_three(layer, index):
    global total
    first = dict_tri[layer + 1][index]
    second = dict_tri[layer + 1][index + 1]
    third = dict_tri[layer + 1][index + 2]
    max_number = max(first, second, third)
    total += max_number

    if (max_number == first):
        return index
    elif (max_number == second):
        return index + 1
    else:
        return index + 2


m = 0
first_index = 0
first_layer = 0
total += dict_tri[0][0]
while m < depth - 1:
    max_index = check_three(first_layer, first_index)
    #print(max_index)
    m += 1
    first_layer += 1
    first_index = max_index


#print(total)
#print(dict_tri[2])
