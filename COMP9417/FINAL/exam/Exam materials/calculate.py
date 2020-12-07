def num(n):
    if n == 0:
        return 1
    else:
        return n * num(n - 1)


list_rate_1 = [0.2174, 0.1304, 0.3913, 0.2609]
list_occur_1 = [5, 3, 9, 6]


list_rate_2 = [0.6, 0.2, 0.05, 0.15]
list_occur_2 = [12, 4, 1 ,3]


result = 0 + num(20)

for i in range(4):
    up = pow(list_rate_2[i], list_occur_2[i])
    down = num(list_occur_2[i])
    res = up / down
    result *= res

print(result)