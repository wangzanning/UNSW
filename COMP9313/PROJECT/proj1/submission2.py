## import modules here

########## Question 1 ##########
# do not change the heading of the function
def c2lsh(data_hashes, query_hashes, alpha_m, beta_n):

    #check the difference satisfy the offset given
    def check_satisfy(difference, alpha_m, offset):
        counter = 0
        for i in range(len(difference)):
            if difference[i] <= offset:
                counter = counter + 1
        if counter >= alpha_m:
            return True
        else:
            return False

    #create a list to store the difference of data and query in advance
    def check_diff(data, query):
        output = []
        for i in range(len(data)):
            output.append(abs(data[i]-query[i]))
        return output

    #change the data_hashes to [hashes, difference, data]
    data_hashes = data_hashes.map(lambda e : (e[0], check_diff(e[1], query_hashes), e[1]))

    offset = -1
    while True:
        offset = offset + 1
        #filter the data_hashes with satisfy the offset
        data_hashes = data_hashes.filter(lambda e : check_satisfy(e[1], alpha_m, offset) )
        number_of_satisfy = data_hashes.count()

        #check the number of query satisfy the beta_n
        if number_of_satisfy >= beta_n:
            # get the hashes from the rdd_data
            output = data_hashes.map(lambda e: e[0])
            break

        #print("offset: ", offset, "numCandidates: ", number_of_satisfy)
    return output



