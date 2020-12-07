# spiral.py
# COMP9444, CSE, UNSW

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

class PolarNet(torch.nn.Module):
    def __init__(self, num_hid):
        super(PolarNet, self).__init__()
        self.linear_func_1 = nn.Linear(2, num_hid)
        self.linear_func_2 = nn.Linear(num_hid, 1)
        self.tanh = nn.Tanh()
        self.sigmod = nn.Sigmoid()

    def forward(self, input):
        x = input[:, 0]
        y = input[:, 1]
        # get the sqrt(x2,y2)
        r = torch.norm(input, 2, dim=-1)
        a = torch.atan2(y, x)
        input_layer = torch.stack((r, a), 1)
        first_layer = self.linear_func_1(input_layer)
        self.print_layer = self.tanh(first_layer)
        output_layer = self.sigmod(self.linear_func_2(self.print_layer))
        return output_layer

class RawNet(torch.nn.Module):
    def __init__(self, num_hid):
        super(RawNet, self).__init__()
        # INSERT CODE HERE
        self.linear_func_1 = nn.Linear(2, num_hid)
        self.linear_func_2 = nn.Linear(num_hid, num_hid*2)
        self.hidden = nn.Linear(num_hid*2, 1)
        self.tanh = nn.Tanh()
        self.sigmod = nn.Sigmoid()
        self.relu = nn.ReLU()


    def forward(self, input):
        input_layer = self.linear_func_1(input)
        first_layer = self.tanh(input_layer)
        self.second_layer = self.linear_func_2(first_layer)
        self.print_layer = self.tanh(self.second_layer)
        output_layer = self.sigmod(self.hidden(self.print_layer))
        return output_layer

def graph_hidden(net, layer, node):
    # plt.clf()
    # INSERT CODE HERE
    # changed based on the function graph_output() in the spiral_main
    xrange = torch.arange(start=-7, end=7.1, step=0.01, dtype=torch.float32)
    yrange = torch.arange(start=-6.6, end=6.7, step=0.01, dtype=torch.float32)
    xcoord = xrange.repeat(yrange.size()[0])
    ycoord = torch.repeat_interleave(yrange, xrange.size()[0], dim=0)
    grid = torch.cat((xcoord.unsqueeze(1), ycoord.unsqueeze(1)), 1)

    with torch.no_grad():  # suppress updating of gradients
        net.eval()  # toggle batch norm, dropout
        net(grid)
        if layer == 1:
            output = net.print_layer[:, node]
        else:
            output = net.print_layer[:, node]

        net.train()

        pred = (output >= 0.5).float()

        # plot function computed by model
        plt.clf()
        plt.pcolormesh(xrange, yrange, pred.cpu().view(yrange.size()[0], xrange.size()[0]), cmap='Wistia')

