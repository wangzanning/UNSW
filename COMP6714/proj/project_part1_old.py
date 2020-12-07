import copy

def WAND_Algo(query_terms, top_k, inverted_index):
    # print(query_terms)
    print(top_k)
    # print(inverted_index)
    data = []
    end_counter = 0
    threshold = 0
    used_inverted_index = {}
    output_first = []
    output_second = 0
    # select used word in inverted_index
    for i in query_terms:
        used_inverted_index[i]=inverted_index[i]
    # build a new form to store the data
    for i in used_inverted_index:
        invert_list = [{'word':i, 'new_invert': used_inverted_index[i]}]
        data.append(invert_list)
    print('data',data)
    # create a dict to store index
    dict_index = {}
    for i in range(len(query_terms)):
        temp = 'word' + str(i)
        dict_index[temp] = 0
    data_invert_dict = []
    # translate inverted_index into dict
    for i in data:
        temp = i[0]['new_invert']
        temp_dict = {}
        for i in temp:
            temp_dict[i[0]] = i[1]
        data_invert_dict.append(temp_dict)
    # print(data_invert_dict)
    current_index_list = []
    # initial the index of each word
    for i in range(len(query_terms)):
        current_index_list.append(dict_index['word' + str(i)])
    data_length_list = []
    for i in data_invert_dict:
        data_length_list.append(len(i))
    print('data_length',data_length_list)
    max_length_word = max(data_length_list)
    index_while = 0
    pivot_index = -1

    # check at the end of the each word list
    # while index_while < max_length_word:
    while end_counter < len(query_terms):
        print('threshold',threshold)
    # test = 0
    # while test < 10:
    #     test += 1
        end_counter = 0
        #get the upperbound of each word
        upperBound_list = []
        for i in data:
            temp = i[0]['new_invert']
            largest_num = 0
            for i in temp:
                if i[1] > largest_num:
                    largest_num = i[1]
            upperBound_list.append(largest_num)
        # print(upperBound_list)
        current_index_value = []      #[current index_value, upperbound, word_index]
        print('pointer',current_index_list)
        # check if the index at the end of each term
        for i in range(len(current_index_list)):
            if current_index_list[i] == data_length_list[i]-1 or current_index_list[i] == data_length_list[i]:
                end_counter += 1
        # if end_counter == len(query_terms):
        #     break
        print('end_counter',end_counter)
        # get the current index value of each word
        for i in range(len(data)):
            try:
                temp = data[i][0]['new_invert'][current_index_list[i]]
            except:
                pass
            else:
                res = (temp, upperBound_list[i], i, data_length_list[i])
                current_index_value.append(res)
        current_index_value = sorted(current_index_value)
        print('current_index_value',current_index_value)
        # get pivot
        pivot_counter = 0
        for i in range(len(current_index_value)):
            pivot_counter += current_index_value[i][1]
            if pivot_counter > threshold:
                pivot_index = i
                break
        print('pivot_index',pivot_index)
        # line 20 check case2: when the c_pivot = c0
        current_score = 0
        print('data_invert_dict',data_invert_dict)
        if current_index_value[pivot_index][0][0] == current_index_value[0][0][0]:
            # output_second += 1
            current_pivot_DocId = current_index_value[pivot_index][0][0]
            print('current_pivot_DocId',current_pivot_DocId)
            i = 0
            check_threshold = 0
            while i < len(query_terms):
                temp_score = data_invert_dict[i].get(current_pivot_DocId, 0)
                current_score += temp_score
                if temp_score != 0:
                    for term in current_index_value:
                        if term[2] == i:
                            check_threshold += term[1]
                i+=1
            print('score',current_score)
            # check the sum of current upperbound over the threshold, add full evaluation
            if check_threshold > threshold:
                output_second += 1
            #  move the index to the next one
            i = 0
            while i < len(query_terms):
                temp_score = data_invert_dict[i].get(current_pivot_DocId, 0)
                print(temp_score)
                if temp_score != 0:
                    if current_index_value[i][0][0] == current_pivot_DocId:
                        print('123')
                        update_index = current_index_value[i][2]
                        # if current_index_list[update_index] < current_index_value[i][3]:
                        current_index_list[update_index] += 1
                i += 1
            index_while += 1
            # print('new_pointer', current_index_list)
            # check the current number in the output list exceed top-k
            if current_score > threshold:
                output_first.append((current_score, current_index_value[pivot_index][0][0]))
            # check the smallest one, update the threshold according to the top-k
            # print(output_first)
            if len(output_first) > top_k:
                output_first = sorted(output_first)
                del output_first[0]
                threshold = output_first[0][0]
            print('output_first',output_first)
            print('case2')
            print('-------------------------------------')
        # line 35 case1: move the term before pivot to the next index
        else:
            for i in range(pivot_index):
                update_index = current_index_value[i][2]
                for k in range(len(data[update_index][0]['new_invert'])):
                    current_pivot_DocId = current_index_value[pivot_index][0][0]
                    if data[update_index][0]['new_invert'][k][0] >= current_pivot_DocId:
                        current_index_list[update_index] = k
                        break
            index_while += 1
            print('case1')
            print('-------------------------------------')
            # print('2',current_index_list)

    sorted_list = sorted(output_first, key=lambda x: x[1] ,reverse=False)
    output_first = sorted(sorted_list, key=lambda x: x[0], reverse=True)

    print('final',output_first)
    print('output_second',output_second)
    print('-------------------------------------')
    return output_first, output_second
