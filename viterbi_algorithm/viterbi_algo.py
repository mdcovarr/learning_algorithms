# Michael Covarrubias
# PID#: A12409694
# Email: mdcovarr@ucsd.edu

import numpy as np
import math
import operator
import matplotlib.pyplot as plt

#TODO fix this shit!! it doth not work 

class viterbi_algo:
    def __init__(self, e_data, init_data, observe_data, trans_data):
        self.e_data = e_data
        self.init_data = init_data
        self.observe_data = observe_data
        self.trans_data = trans_data
        self.l = np.zeros((len(trans_data[:,0]), len(observe_data[0,:])))
        self.max_index = np.zeros((1,len(observe_data[0,:])))

    def base_case(self):
        t = 0
        i = 0
        index = 0
        maxVal = -100.0

        while i < len(self.init_data[:,0]):
            out = self.observe_data[0,0]

            if out == '1':
                b = math.log(float(self.e_data[i,1]))
            else:
                b = math.log(float(self.e_data[i,0]))

            pi = math.log(float(self.init_data[i,0]))
            l = pi + b

            if l > maxVal:
                maxVal = l
                index = i
            self.l[i,0] = l
            i += 1
        self.max_index[0,t] = index

    def forward_pass(self, t_1):
        ''' remember that t starts at 0 and not 1 '''
        t = t_1 - 1
        i = int(self.max_index[0,t])
        max_l = self.l[i, t]
        out = self.observe_data[0,t_1]
        out = int(out)
        max_val = -100000.0
        max_index = -1
        j = 0

        while j < len(self.init_data[:,0]):
            a = math.log(float(self.trans_data[i,j]))
            b = math.log(float(self.e_data[j,out]))
            l = (max_l + a) + b
            self.l[j, t_1] = l

            if l > max_val:
                max_index = j
                max_val = l

            j += 1
        self.max_index[0,t_1] = max_index

if __name__ == '__main__':
    e_file = open('emissionMatrix.txt', 'r')
    e_data = np.array([line.rstrip().split("\t") for line in e_file])
    e_file.close

    init_state_file = open('initialStateDistribution.txt', 'r')
    init_data = np.array([line.rstrip().split(" ") for line in init_state_file])
    init_state_file.close

    observe_file = open('observations.txt', 'r')
    observe_data = np.array([line.rstrip().split(" ") for line in observe_file])
    observe_file.close

    trans_file = open('transitionMatrix.txt', 'r')
    trans_data = np.array([line.rstrip().split(" ") for line in trans_file])
    trans_file.close

    data = viterbi_algo(e_data, init_data, observe_data, trans_data)

    data.base_case()
    i = 1

    while i < len(data.observe_data[0,:]):
        data.forward_pass(i)
        i += 1

    i = 0
    while i < len(data.max_index[0,:]):
        print (data.max_index[0,i])
        i += 1
