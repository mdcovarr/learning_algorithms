# Michael Covarrubias
# PID#: A12409694
# Email: mdcovarr@ucsd.edu

import numpy as np
import math
import operator

class mdp:
    def __init__(self, data_a1, data_a2, data_a3, data_a4, rewards):
        self.data_a1 = data_a1
        self.data_a2 = data_a2
        self.data_a3 = data_a3
        self.data_a4 = data_a4
        self.rewards = rewards
        self.values = np.zeros(len(self.rewards[:,0]))
        self.prev_values = np.zeros(len(self.rewards[:,0]))
        self.policy = [None]*len(self.rewards[:,0])

    def max_a_summation(self, s):
        a = 0
        curr_max = -100000.0
        ''' first iterate through all 4 actions a = 1,2,3,4 '''
        while a < 4:
            if a == 0:
                curr_data = self.data_a1
            if a == 1:
                curr_data = self.data_a2
            if a == 2:
                curr_data = self.data_a3
            if a == 3:
                curr_data = self.data_a4

            curr_sum = 0.0
            x = 0
            ''' Next iterate through each file '''
            while x < len(curr_data[:,0]):
                if int(curr_data[x,0]) == (s+1):
                    curr_sum += float(curr_data[x,2]) * self.prev_values[int(curr_data[x,1])-1]
                x += 1
            ''' determine if you have a new max based on action '''
            if curr_sum > curr_max:
                curr_max = curr_sum
                a_max = a
            a += 1
        ''' return max summation '''
        return_vals = [curr_max, a_max]
        return return_vals

    def value_iteration(self, k_max):
        k = 1;
        gamma = 0.9925

        ''' k is number of iternations we want to run algo for '''
        while k < k_max:
            self.prev_values = self.values
            s = 0
            ''' this loop will update all V(k+1) '''
            while s < len(self.values[:]):
                r_s = int(self.rewards[s,0])

                ''' find max a (action) '''
                max_vals = self.max_a_summation(s)
                max_sum = max_vals[0]

                ''' need to use max_a to determine pi(s) '''
                max_a = max_vals[1]
                direct = self.policy_update(s, max_a)
                self.policy[s] = direct
                self.values[s] = r_s + (gamma * float(max_sum))
                s += 1
            k += 1

    def policy_update(self, s, a):
        if a == 0:
            direction = 'WEST'
        if a == 1:
            direction = 'NORTH'
        if a == 2:
            direction = 'EAST'
        if a == 3:
            direction = 'SOUTH'
        return direction

if __name__ == "__main__":
    file_a1 = open('hw7_prob_a1.txt', 'r')
    data_a1 = np.array([line.strip().split("   ") for line in file_a1])
    file_a1.close

    file_a2 = open('hw7_prob_a2.txt', 'r')
    data_a2 = np.array([line.strip().split("   ") for line in file_a2])
    file_a2.close

    file_a3 = open('hw7_prob_a3.txt', 'r')
    data_a3 = np.array([line.strip().split("   ") for line in file_a3])
    file_a3.close

    file_a4 = open('hw7_prob_a4.txt', 'r')
    data_a4 = np.array([line.strip().split("   ") for line in file_a4])
    file_a4.close

    reward_file = open('hw7_rewards.txt', 'r')
    rewards = np.array([line.strip().split("   ") for line in reward_file])
    reward_file.close

    data = mdp(data_a1, data_a2, data_a3, data_a4, rewards)
    data.value_iteration(1000)

    i = 0
    ''' A quick print out of all values of maze numbers '''
    while i < len(data.values[:]):
        if data.rewards[i] == '-1':
            data.policy[i] = 'DRAGON'
        if data.rewards[i] == '1':
            data.policy[i] = 'EXIT'
        if data.values[i] != 0.0:
            print (str(i+1) + ':\t\t' + str(data.values[i]) + '\t\t' + str(data.policy[i]))
        i += 1
