# by Elijah DengDeng

import pickle
import random

# dummyList = [1,2,3,4,5]
#
# with open('testCases/dummy.pkl', 'wb') as f:
#     pickle.dump( dummyList, f )
#
# with open('testCases/dummy.pkl', 'rb') as f:
#     showList = pickle.load(f)
#
# print(showList)

# 20w data with same hashCode
# allWithOneSameCode = [[ 0 for _ in range(32) ] for _ in range(200000)]
#
# with open('testCases/testCase0.pkl', 'wb') as f:
#     pickle.dump( allWithOneSameCode, f )
#
# with open('testCases/allWithOneSameCodeQueryHash.pkl', 'rb') as f:
#     showList = pickle.load(f)
#
# print(len(showList))
# print(showList)

# 20w data/ 32bit hashCode/ 5w data having the same hash with query /
# other 5w data is matched with query with offset = 10

offet  = 10
sameAsQuery = [ [0 for _ in range(32)]  for _ in range(50000)]
matchWithQueryOffSet10 = [ [random.randint(-10, 10) for _ in range(32)] for _ in range(50000)]
otherRandom = [[random.randint(20, 40) for _ in range(32)] for _ in range(100000) ]
r = sameAsQuery + matchWithQueryOffSet10 + otherRandom
random.shuffle(r)

with open('testCases/testQueryHash.pkl', 'wb') as f:
    pickle.dump( [ 0 for _ in range(32) ], f )

with open('testCases/testCase1.pkl', 'wb') as f:
    pickle.dump( r, f )

# with open('testCases/testCase1.pkl', 'rb') as f:
#     showList = pickle.load(f)
#
# print( len(showList) )
# print( len(showList[0]) )


# 100w data/ 32bit hashCode/ 5w data having the same hash with query /
# other 5w data is matched with query with offset = 10

sameAsQuery = [ [0 for _ in range(32)]  for _ in range(50000)]
matchWithQueryOffSet10 = [ [random.randint(-10, 10) for _ in range(32)] for _ in range(50000)]
otherRandom = [[random.randint(20, 40) for _ in range(32)] for _ in range(900000) ]
r = sameAsQuery + matchWithQueryOffSet10 + otherRandom
random.shuffle(r)

with open('testCases/testCase2.pkl', 'wb') as f:
    pickle.dump( r, f )

with open('testCases/testCase2.pkl', 'rb') as f:
    showList = pickle.load(f)

print( len(showList) )
print( len(showList[0]) )
