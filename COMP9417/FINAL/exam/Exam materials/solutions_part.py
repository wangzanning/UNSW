## Question 2

import numpy as np

x0 = [1, 1, 1, 1, 1, 1, 1, 1]
x1 = [-0.8, 3.9, 1.4, 0.1, 1.2, -2.45, -1.5, 1.2]
x2 = [1, 0.4, 1, -3.3, 2.7, 0.1, -0.5, -1.5]
y = [1, -1, 1, -1, -1, -1, 1, 1]

np_x0 = np.asarray(x0)
np_x1 = np.asarray(x1)
np_x2 = np.asarray(x2)
np_y = np.asarray(y)
w_start = [1.00,1.00,1.00]
learning_rate = 0.2
counter = 0

def check_positive(x0, x1, x2, y):
    print("--------------------")
    global w_start, counter
    wTx = (w_start[0] * x0) + (w_start[1] * x1) + (w_start[2] * x2)
    ywTx = wTx * y

    if ywTx >= 0:
        counter += 1
    else:
        w_start = [w_start[0] - y * (learning_rate * x0), w_start[1] - y * (learning_rate * x1), w_start[2] - y * (learning_rate * x2) ]

print("φ(xi)        yiφT(xi)w*")
counter2 = 0
while True:
    counter = 0
    for i in range(8):
        check_positive(np_x0[i],np_x1[i], np_x2[i], np_y[i])
        list_w = [w_start[0], w_start[1], w_start[2]]

        if list_w:
            b = "ri > 0"
        print(list_w, b )
    if counter == 8:
        break

    counter2 +=1
    if counter2 == 100:
        break

#print((np_x0[2]))




