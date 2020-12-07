action = int(input())
k = 0
dict_action = {}
action_time = 0
new_list = []

while k <= action - 1:
    dict_action[k] = [int(i) for i in input().split()]
    k = k + 1

def action_1(a, b):
    new_list.insert(a,b)


def action_2(a):
    new_list.pop(a)

def action_3():
    for i in new_list:
        print(i, end=" ")

m = 0

while m < action:

    if dict_action[m][0] == 1:
        dict_action.pop(0)
        while dict_action[m]:
            index = 0
            action_1(dict_action[m][index],dict_action[m][index+1])
            dict_action.pop(0, 1)

    elif dict_action[m][0] == 2:
        dict_action.pop(0)
        while dict_action[m]:
            index = 0
            action_2(dict_action[m][index])
            dict_action.pop(0)
    else:
        action_3()
    m += 1

#print(dict_action[1][2])


