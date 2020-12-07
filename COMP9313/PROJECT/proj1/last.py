#!/usr/bin/env python
# coding: utf-8
def c2lsh(datas, querys, a_m, b_n):
    n_offset = -1
    n_can = -1
    datas = datas.map(lambda e : (e[0],diff(e[1],querys)))
    while n_can < b_n: 
        n_offset += 1
        # filter + map => flatMap
        RDD = datas.flatMap(lambda e : [e[0]] if is_cand(e[1],a_m,b_n) else [])
        n_can = RDD.count()
        print("number of offset: ", b_n, "number of Candidates: ", n_can)

    return RDD



# diff函数移出来
def diff(data1,query1):
    n_data = len(data1)
    dif=list()
    for i in range(n_data):
        dif.append(abs(data1[i]-query1[i]))
    return dif


# check if dataHashCode is qualifited for appending candidates
def is_cand(a_diff , a_m, b_n):
    # dataHashCode, queryHashCode string
    # alpha_m, int
    # beta_n, int
    sum_0 = 0
    n_len = len(a_diff)
    for i in range(n_len):
        if a_diff[i] <= b_n:
            sum_0 += 1
        if sum_0>=a_m:
            return True
    return False


# In[ ]:




