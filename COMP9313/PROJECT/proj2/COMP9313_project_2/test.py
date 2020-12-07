count = int(input())
arr = [int(i) for i in input().split()]

total = 0

for i in range(count):
    total += arr[i]

check_sum = total % 10
sort_arr = sorted(arr)
#print(sort_arr)

if (check_sum == 5):
    for i in range(count):
        if (sort_arr[i] != 10):
            total = total - sort_arr[i]
            break
    print(total)
else:
    print(total)