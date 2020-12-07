#!/usr/bin/env python3
"""
student.py
Name: Zanning Wang
zID: z5224151
UNSW COMP9444 Neural Networks and Deep Learning

"""


import torch
import re
import torch.nn as tnn
import torch.optim as toptim
from torchtext.vocab import GloVe
# import numpy as np
# import sklearn

from config import device

################################################################################
#####
#In order to solve the long dependency problem of text prediction in neural network learning,
# we choose the LSTM model in RNN to make the prediction in current assignment. At first, we make
# preprocessing to the sample text, by removing the unnecessary character such as ' ,'',[,] and
# lowercase the input, and we also add the stopwords to help make pause when training, the stop
# words is refer from "nltk.corpus".
#
# In convertNetOutput, We constrain the data within the corresponding range and output the output
# according to the max value in each vector, I forget use Argmax which is built-in method at first
# and Achieve the same effect with my own code
#
# In the Network part, we apply one layer LSTM model and two layer full-connected model for each category
# input and layer_input, use RELU between each full-connected layer, set the batch first at first try, use the
# MSEloss in the loss part, the score can reach about 78, In the next optimization process, we set the
# number of layer as 2 and set dropout as 0.5, to avoid overfitting.
#
# I also found by changing the MSEloss into CrossEntrophyLoss may have a little help to increase the accuracy
# and also change the optimiser from SGD into Adam.
#
# ######
################################################################################

def tokenise(sample):
    """
    Called before any processing of the text has occurred.
    """

    processed = sample.split()

    return processed

def preprocessing(sample):
    """
    Called after tokenising but before numericalising.
    """
    # remove unnecessary character and lower the sample, also check they were in
    processing_list = []
    for i in sample:
      i = re.sub("[^a-zA-Z\d]", ' ', i).lower()
      if i !=' ' and i not in stopWords:
        processing_list.append(i)

    return processing_list

def postprocessing(batch, vocab):
    """
    Called after numericalising but before vectorising.
    """

    return batch

stopWords = {'a', 'an', 'ain', 'aren','as', 'i', 'me', 'my', 'myself', 'we','don', 'should', 'now', 'd', 'll', 'm', 'our',
             'ours', 'ourselves', 'you', 'your','yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
             'some', 'such', 'no', 'nor', 'not', 'themselves', 't', 'can','they', 'them', 'their', 'what', 'which', 'who',
             'whom', 'this', 'that', 'these','those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
             'had', 'having', 'do','does', 'did', 'doing', 'the', 'and', 'but', 'if', 'or', 'because',  'until', 'while',
            'of', 'at', 'by', 'for', 'with', 'about',  'herself', 'it', 'its', 'itself','too', 'very', 's', 'theirs', 'other'
            'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'once', 'here','against', 'between', 'into', 'through', 'shouldn', 'wasn', 'weren', 'during','will',
             'just',  'o', 're', 've','further', 'then', 'before', 'there', 'when', 'where', 'why',
             'how', 'all', 'any', 'both', 'each','couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn',
            'needn', 'shan', 'won', 'wouldn'}
wordVectors = GloVe(name='6B', dim=100)

################################################################################
####### The following determines the processing of label data (ratings) ########
################################################################################

def convertNetOutput(ratingOutput, categoryOutput):

    # Restrict text in scope
    ratingOutput = torch.clamp(ratingOutput, 0, 1)
    categoryOutput = torch.clamp(categoryOutput, 0, 4)
    # get the index of the largest value from each vector
    rating_result = []
    for i in ratingOutput:
      i = i.tolist()
      rating_result.append(i.index(max(i)))
    rating_result = torch.tensor(rating_result, dtype=torch.long)

    cate_result = []
    for i in categoryOutput:
      i = i.tolist()
      cate_result.append(i.index(max(i)))
    cate_result = torch.tensor(cate_result,dtype = torch.long)
    # print(ratingOutput.shape)
    # rating_result = torch.argmax(ratingOutput, dim=-1)
    # cate_result = torch.argmax(categoryOutput, dim=-1)
    return rating_result.to(device), cate_result.to(device)

################################################################################
###################### The following determines the model ######################
################################################################################

class network(tnn.Module):

    # use LSTM as the basic model, set number of layer as 2 and add dropout
    def __init__(self):
        super(network, self).__init__()
        hidden_size = 300
        self.lstm = tnn.LSTM(input_size=100, hidden_size = hidden_size, batch_first=True, num_layers=2,dropout=0.5)
        self.fullConnect_1 = tnn.Linear(hidden_size, 128)
        self.fullConnect_2 = tnn.Linear(128, 2)
        self.fullConnect_3 = tnn.Linear(hidden_size, 128)
        self.fullConnect_4 = tnn.Linear(128, 5)
        self.relu = tnn.ReLU()

    def forward(self, input, length):
        input = tnn.utils.rnn.pack_padded_sequence(input, length.cpu(), batch_first=True)
        output,(hnn, cnn) = self.lstm(input)
        layer_fc1 = self.fullConnect_1(hnn[1])
        layer_relu = self.relu(layer_fc1)
        layer_fc2 = self.fullConnect_2(layer_relu)
        rating_result = layer_fc2.reshape(-1,2)

        layer_fc1 = self.fullConnect_3(hnn[1])
        layer_relu = self.relu(layer_fc1)
        layer_fc2 = self.fullConnect_4(layer_relu)
        category_result = layer_fc2.reshape(-1,5)
        #print(rating_result.shape)

        return rating_result, category_result

class loss(tnn.Module):

    # use CrossEntropyLoss
    def __init__(self):
        super(loss, self).__init__()
        self.crossLoss = tnn.CrossEntropyLoss()

    def forward(self, ratingOutput, categoryOutput, ratingTarget, categoryTarget):
        ratingLoss = self.crossLoss(ratingOutput, ratingTarget)
        categoryLoss = self.crossLoss(categoryOutput, categoryTarget)
        output = ratingLoss + categoryLoss
        return output

net = network()
lossFunc = loss()

################################################################################
################## The following determines training options ###################
################################################################################

trainValSplit = 0.8
batchSize = 32
epochs = 10
# optimiser = toptim.SGD(net.parameters(), lr=0.01)
# change teh optimeser from SGD into ADSM
optimiser = toptim.Adam(net.parameters(), lr=0.002)

