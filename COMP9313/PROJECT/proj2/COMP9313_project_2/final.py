def collision_count(a, b, offset):
    counter = 0
    for i in range(len(a)):

        if abs(a[i] - b[i]) <= offset:
            counter += 1
    return counter


def c2lsh(data_hashes, query_hashes, alpha_m, beta_n):
    offset = 0
    cand_num = 0
    while cand_num < beta_n:
        candidates = data_hashes.flatMap(
            lambda x: [x[0]] if collision_count(x[1], query_hashes, offset) >= alpha_m else [])

        cand_num = candidates.count()

        offset += 1
    return candidates
