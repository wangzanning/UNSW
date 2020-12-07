number = int(input())
count = int(input())
arr = [int(i) for i in input().split()]

person1 = []
person2 = []

sort_arr = sorted(arr)
sort_arr.reverse()
# print(sort_arr)
same_value = 0
person1.append(sort_arr[0])

for i in range(1, count):

    if sum(person1) > sum(person2):
        person2.append(sort_arr[i])

    elif sum(person1) < sum(person2):
        person1.append(sort_arr[i])

    else:
        same_value = sum(person1)
        person1.append(sort_arr[i])


output = sum(sort_arr) - 2 * same_value
print(output)




