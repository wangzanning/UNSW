# version 2
# add groupByKey
# add flag
# by Elijah DengDeng

def c2lsh(data_hashes, query_hashes, alpha_m, beta_n):

    offset = -1
    numCandidates = -1

    # add groupByKey
    shuffledHashRDD = data_hashes.map(lambda e: (tuple(e[1]), e[0])).groupByKey() \
        .map(lambda e: (e[0], e[1], False))

    while numCandidates < beta_n: 
        offset += 1

        shuffledHashRDD = shuffledHashRDD.map(lambda e : (e[0], e[1], True if e[2] else ifqualified( e[0], query_hashes, alpha_m, offset )))

        # filter + map => flatMap
        candidatesRDD = shuffledHashRDD.flatMap(lambda e : e[1] if e[2] else [])

        numCandidates = candidatesRDD.count()
    return candidatesRDD


# check if dataHashCode is qualifited for appending candidates
def ifqualified(dataHashCode , queryHashCode, alpha_m, offset):
    # dataHashCode, queryHashCode string
    # alpha_m, int
    # offset, int
    count = 0
    length = len(dataHashCode)
    for i in range(length):
        if ( abs(dataHashCode[i] - queryHashCode[i]) <= offset):
            count += 1
    return count >= alpha_m