data=[1,3,2,1,4,5,3,3,4,2]
query=[2,3,4,5,6,4,3,4,5,6]
output=[]

for i in range (10):
    output.append(abs(data[i]-query[i]))
output2=[abs(data[i]-query[i]) for i in range(10)]

print(output)
print(output2)
