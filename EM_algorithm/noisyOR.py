# Michael Covarrubias
# PID#: A12409694
# Emial: mdcovarr@ucsd.edu

import numpy as np
import math
import operator
import matplotlib.pyplot as plt

class noisyOR:
    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data
        self.p_i = np.ones(len(self.x_data[0,:]))
        self.p_i /= len(self.x_data[0,:])
        self.products = np.zeros(len(self.x_data[:,0]))
        self.m = 0
        self.l = 0.0

    def calculate_product(self, t):
        product = 1.0
        i = 0

        while i < len(self.x_data[0,:]):
            exp = int(self.x_data[t,i])
            val = (1.0 - self.p_i[i])
            product *= math.pow(val, exp)
            i += 1
        self.products[t] = product
        return product

    def max_likelihood(self):
        t = 0
        m = 0
        total = 0.0

        while t < len(self.y_data[:,0]):
            product = self.calculate_product(t)

            if int(self.y_data[t,0]) == 1:
                prob = 1.0 - product
                if prob <= 0.50:
                    m += 1
            else:
                prob = product
                if prob < 0.50:
                    m += 1

            total += math.log(prob)
            t += 1
        l = total / (len(self.y_data[:,0]) * 1.0)
        self.l = l
        self.m = m

    def update_p_i(self):
        i = 0

        while i < len(self.p_i[:]):
            t = 0
            t_i = 0
            total = 0.0
            while t < len(self.x_data[:,0]):

                if int(self.x_data[t,i]) == 1:
                    t_i += 1

                num = int(self.y_data[t,0]) * int(self.x_data[t,i]) * self.p_i[i] * 1.0
                den = 1.0 - self.products[t]
                total += (num / den)

                t += 1
            self.p_i[i] = (total / t_i)
            i += 1

if __name__ == "__main__":
    x_file = open('hw5_noisyOr_x.txt', 'r')
    x_data = np.array([line.rstrip().split(" ") for line in x_file])
    x_file.close

    y_file = open('hw5_noisyOr_y.txt', 'r')
    y_data = np.array([line.rstrip().split(" ") for line in y_file])
    y_file.close

    total_count= 512
    print_set = set([0, 1, 2, 4, 8, 16, 32, 64, 128, 256])
    i = 0
    data = noisyOR(x_data, y_data)

    while i < total_count:
        data.max_likelihood()
        data.update_p_i()
        if i in print_set:
            print (str(i) + ':\t' + 'Mistakes: ' + str(data.m) + '\tLikelihood: ' + str(data.l))
        i += 1
    print (str(i) + ':\t' + 'Mistakes: ' + str(data.m) + '\tLikelihood: ' + str(data.l))

    i = 0
    while i < len(data.p_i[:]):
        print (str(i) + ':\t' + str(data.p_i[i]))
        i += 1
