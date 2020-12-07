# by Elijah DengDeng

def c2lsh(data_hashes, query_hashes, alpha_m, beta_n):
    offset = -1
    numCandidates = -1
    def diff(data_hash, query_hash):
        length = len(data_hash)
        return [abs(data_hash[i] - query_hash[i]) for i in range(length)]

    data_hashes = data_hashes.map(lambda e : (e[0], diff(e[1], query_hashes)))
    while numCandidates < beta_n:
        offset += 1 #(0)
        # e : (id, difference)
        candidatesRDD = data_hashes.flatMap( lambda e : [e[0]] if ifQualified(e[1], alpha_m, offset) else [])
        numCandidates = candidatesRDD.count()

        print("offset: ", offset,  "numCandidates: ", numCandidates)
    return candidatesRDD

def ifQualified(difference, alpha_m, offset):
    count = 0
    length = len(difference)
    for i in range( length ):
        if difference[i] <= offset:
            count += 1
        if count >= alpha_m:
            return True
    return False
