# kuzu.py
# COMP9444, CSE, UNSW

from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F

class NetLin(nn.Module):
    # linear function followed by log_softmax
    def __init__(self):
        super(NetLin, self).__init__()
        # INSERT CODE HERE
        self.linear_func = nn.Linear(28*28,10)
        self.softmax = nn.LogSoftmax()

    def forward(self, x):
        input_layer = x.view(x.shape[0], -1)
        full_connection = self.linear_func(input_layer)
        output_layer = self.softmax(full_connection)
        return output_layer


class NetFull(nn.Module):
    # two fully connected tanh layers followed by log softmax
    def __init__(self):
        super(NetFull, self).__init__()
        # INSERT CODE HERE
        self.linear_func_1 = nn.Linear(28*28, 70)
        self.linear_func_2 = nn.Linear(70, 10)
        self.tanh = nn.Tanh()
        self.softmax = nn.LogSoftmax()

    def forward(self, x):
        input_layer = x.view(x.shape[0], -1)
        first_layer = self.tanh(self.linear_func_1(input_layer))
        second_layer = self.linear_func_2(first_layer)
        output_layer = self.softmax(second_layer)

        return output_layer

class NetConv(nn.Module):
    # two convolutional layers and one fully connected layer,
    # all using relu, followed by log_softmax
    def __init__(self):
        super(NetConv, self).__init__()
        self.convol_layer_1 = nn.Conv2d(1, 15, kernel_size=5)
        self.convol_layer_2 = nn.Conv2d(15, 50, kernel_size=5)
        self.linear_func_1 = nn.Linear(800, 300)
        self.linear_func_2 = nn.Linear(300, 10)
        self.maxpool = nn.MaxPool2d(2)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.softmax = nn.LogSoftmax()


    def forward(self, x):
        first_layer = self.relu(self.maxpool(self.convol_layer_1(x)))
        second_layer = self.relu(self.maxpool(self.convol_layer_2(first_layer)))
        view_layer = second_layer.view(x.shape[0], -1)
        third_layer = self.relu(self.linear_func_1(view_layer))
        output_layer = self.softmax(self.linear_func_2(third_layer))

        return output_layer
