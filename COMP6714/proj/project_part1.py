def WAND_Algo(query_terms, top_k, inverted_index):
    print(query_terms)
    print(top_k)
    # print(inverted_index)
    used_inverted_index = []
    used_inverted_value = []
    data_dict = []
    threshold = 0
    output_first = []
    output_second = 0
    word_length_list = []
    upperbound_list = []
    pivot_index = 0
    # select used word in inverted_index
    for i in query_terms:
        temp = {}
        used_inverted_index.append({i:inverted_index[i]})
    # print(used_inverted_index)
    # get the used inverted index list
    for i in used_inverted_index:
        key = list(i.keys())[0]
        used_inverted_value.append(i[key])
    used_inverted_dict = []
    for i in used_inverted_value:
        temp_dict = {}
        for k in i:
            temp_dict[k[0]] = k[1]
        used_inverted_dict.append(temp_dict)
    # print(used_inverted_value)
    # get the length of each word
    for i in used_inverted_value:
        word_length_list.append(len(i))
    # get the upperbound for each word
    for i in used_inverted_value:
        largest_num = 0
        for k in i:
            if k[1] > largest_num:
                largest_num = k[1]
        upperbound_list.append(largest_num)
    # save data into a form of [{}, {}, {}]

    for i in range(len(query_terms)):
        temp_data = {
            'word':query_terms[i],
            'current':0,
            'upper': upperbound_list[i],
            'length': word_length_list[i],
            'invert': used_inverted_value[i],
            'invert_dict': used_inverted_dict[i]
        }
        data_dict.append(temp_data)
    print(data_dict)
    while len(data_dict) > 0:
        #sort the word according DID
        print('threshold', threshold)
        data_dict.sort(key=lambda x:x['invert'][x['current']])
        #get the pivot
        pivot_counter = 0
        for i in range(len(data_dict)):
            pivot_counter += data_dict[i]['upper']
            if pivot_counter > threshold:
                pivot_index = i
                break
        print('pivot_index', pivot_index)
        # line20: case 2, check if the c_pivot = c_0
        current_score = 0
        pivot_index = 0
        # print(data_dict)
        # print(data_dict[pivot_index])
        if data_dict[pivot_index]['invert'][data_dict[pivot_index]['current']][0] == data_dict[0]['invert'][data_dict[0]['current']][0]:
            # print(data_dict)
            current_pivot_DocId = data_dict[pivot_index]['invert'][data_dict[pivot_index]['current']][0]
            print('current_pivot_DocId', current_pivot_DocId)
            i = 0
            # get the evaluation score
            check_threshold = 0
            while i < len(data_dict):
                temp_score = data_dict[i]['invert_dict'].get(current_pivot_DocId, 0)
                current_score += temp_score
                if temp_score != 0:
                    check_threshold += data_dict[i]['upper']
                i+=1
            print('score', current_score)
            # check the sum of current upperbound over the threshold, add full evaluation
            if check_threshold > threshold:
                output_second += 1
            # move the index to the next one and check if at end of the term
            i = 0
            while i < len(data_dict):
                temp_score = data_dict[i]['invert_dict'].get(current_pivot_DocId, 0)
                if temp_score != 0:
                    current_index_DocId = data_dict[i]['invert'][data_dict[i]['current']][0]
                    if current_index_DocId == current_pivot_DocId:
                        data_dict[i]['current'] += 1
                i+=1
            # check the current number in the output list exceed top-k
            if current_score > threshold:
                output_first.append((current_score, current_pivot_DocId))
            # check the smallest one, update the threshold according to the top-k
            if len(output_first) > top_k:
                output_first = sorted(output_first)
                mini = min(output_first, key=lambda x:x[0])[0]
                mini_same = list(filter(lambda x:x[0] == mini, output_first))
                output_first.remove(sorted(mini_same)[-1])
                threshold = output_first[0][0]
            # check the end of each term
            data_dict = list(filter(lambda x: (x['length'] != x['current']), data_dict))
            print('output_second',output_second)
            print('output_first', output_first)
            print('case2')
            print('-------------------------------------')
        # line 35 case1: move the term before pivot to the next index
        else:
            for i in range(pivot_index):
                current_pivot_DocId = data_dict[pivot_index]['invert'][data_dict[pivot_index]['current']][0]
                print('current_pivot_DocId',current_pivot_DocId)
                for k in range(len(data_dict[i]['invert'])):
                    if data_dict[i]['invert'][k][0] >= current_pivot_DocId:
                        data_dict[i]['current'] = k
                        break
                    else:
                        data_dict[i]['current'] = data_dict[i]['length']
            # check the end of each term
            data_dict = list(filter(lambda x: (x['length'] != x['current']), data_dict))
            print(data_dict)
            print('case1')
            print('-------------------------------------')
    sorted_list = sorted(output_first, key=lambda x: x[1], reverse=False)
    output_first = sorted(sorted_list, key=lambda x: x[0], reverse=True)
    print('final', output_first)
    print('output_second', output_second)
    print('-------------------------------------')
    return output_first, output_second











