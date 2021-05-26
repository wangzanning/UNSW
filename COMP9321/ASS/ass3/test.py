# data = 1
# for i in range(len(data)):
#     data[i] = data[i]+1
# print(data)

# s= [4,3][2>1]
# print(s)

# def test(j):
#     sum = 0
#     if j == 0:
#         sum = 1
#     else:
#         sum = j & test(j - 1)
#     return sum
#
# for i in range(5):
#     print '%d! = %d' % (i ,test(i))
#
# print('\\\t\\')
#12 a b d

# def fib(n):
#     if n ==1:
#         return [1]
#     if n ==2:
#         return [1,1]
#     fibs = [1,1]
#     for i in range(2,n):
#         fibs.append(fibs[-1] + fibs[-2])
#     return fibs

def fib(n):
    if n == 1:
        return [1]
    if n ==2:
        return [1,1]
    fibs = [1,1]
    for i in range(2,n):
        fibs.append(fibs[-1]+fibs[-2])
    return fibs[9]
print(fib(10))
