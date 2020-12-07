#!/usr/bin/env python
# coding: utf-8

# In[ ]:

## import modules here

########## Question 1 ##########
# do not change the heading of the function
def c2lsh(data_hashes, query_hashes, alpha_m, beta_n):
    n_offset = -1
    n_can = -1
    data_hashes = data_hashes.map(lambda e : (e[0],diff(e[1],query_hashes)))
    while n_can < beta_n:
        n_offset += 1
        RDD = data_hashes.flatMap(lambda e : [e[0]] if is_cand(e[1],alpha_m,n_offset) else [])
        n_can = RDD.count()
    return RDD


# In[ ]:


def diff(data1,query1):
    n_data = len(data1)
    dif=list()
    for i in range(n_data):
        dif.append(abs(data1[i]-query1[i]))
    return dif


# In[ ]:


def is_cand(a_diff,alpha_m,offset):
    sum_0 = 0
    n_len = len(a_diff)
    for i in range(n_len):
        if a_diff[i] <= offset:
            sum_0 += 1
    return sum_0 >= alpha_m
