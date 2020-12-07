# for i in range(10):
#     exec(f"temp{i}=0")
# print('111', temp0)
#
# for i in range(10):
#     exec(f"temp{i}=0", globals())
# print('111', temp0)

# test = [(8, 1), (6, 3), (6, 2), (6, 1), (4, 3), (4, 2)]
# test2 = [(8, 1), (6, 1), (6, 2), (6, 3), (4, 2), (4, 3) ]
# sorted_l=sorted(test,key=lambda t:t[1])
# result=sorted(sorted_l,key=lambda t:t[0], reverse=True)
# fl = []
# ll = []
# for f, l in test:
#   fl.append(f)
#   ll.append(l)
# fl.sort(reverse=True)
# ll.sort()
# res = zip(fl,ll)
# for e in res:
#     print(e)
#
# print(test)
#
# test3 = [(6, 1), (6, 2), (6, 3)]
# res = max(test3, key = lambda x : x[0])
# print(res)



# print(same_list)
#
# for i in range(pivot_index):
#     update_index = current_index_value[i][2]
#     current_index_list[update_index] += 1
# index_while += 1
# print('case1')
# print('-------------------------------------')

# data = [{'word': 'the', 'current': 2, 'upper': 4, 'length': 17, 'invert': [(1, 4), (2, 4), (3, 4), (4, 2), (5, 4), (6, 2), (7, 2), (8, 2), (9, 4), (11, 4), (12, 2), (13, 4), (14, 2), (15, 2), (17, 2), (18, 4), (19, 2)]}, {'word': 'Ink', 'current': 0, 'upper': 4, 'length': 1, 'invert': [(1, 4)]}]
#
#
# for i in range(2):
#     index = data[i]['current']
#     data[i]['invert'][index]
# data.sort(key=lambda x:x['invert'][x['current']])
# print(data)



# data_dict = [{'word': 'Microsoft', 'current': 4, 'upper': 6, 'length': 4, 'invert': [(3, 6), (7, 6), (15, 3), (20, 6)], 'invert_dict': {3: 6, 7: 6, 15: 3, 20: 6}}, {'word': 'will', 'current': 5, 'upper': 3, 'length': 5, 'invert': [(4, 3), (12, 3), (13, 3), (15, 3), (18, 3)], 'invert_dict': {4: 3, 12: 3, 13: 3, 15: 3, 18: 3}}, {'word': 'Search', 'current': 0, 'upper': 4, 'length': 1, 'invert': [(10, 4)], 'invert_dict': {10: 4}}]
#
#
# data_dict = list(filter(lambda x: (x['length'] != x['current']), data_dict))
#
# print(data_dict)

data = [(14, 1), (14, 13), (14, 9)]
minest = min(data, key=lambda x: x[0])[0]
data2 = list(filter(lambda x: x[0] == minest, data))
print(minest)
print(sorted(data2)[-1])
print(data)
data.remove(sorted(data2)[-1])
print('data',data)

