R = 20000000
N = 500
K = 200
B = R / N

table = [['*' for _ in range (201)] for _ in range (6)]


table[1][1] = B

for i in range(2, 6):
    table[i][1] = 0

def updateTable(l,k,table):
    if l == 1:
        table[l][k] = k * B -2 * table[2][k] - 3*table[3][k]- 4*table[4][k]- 5*table[5][k]
        return
    table[l][k] = ((6-l) * table[l-1][k-1]) / (N-k+1) +table[l][k-1] - ((6-l-1)*table[l][k-1]) / (N - k +1)
    return


for k in range(2,201):
    for l in (5,4,3,2,1):
        updateTable(l,k,table)
#print()
# for i in table:
#     print(i)
for i in range(1,6):
    print("L{}(200,500) = {}".format(i,table[i][200]))


#print(table[5][200])