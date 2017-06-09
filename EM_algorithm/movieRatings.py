# Name: Michael Covarrubias
# PID#: A12409694
# Email: mdcovarr@ucsd.edu

import numpy as np
import math
import operator
import matplotlib.pyplot as plt

class movieRatings:
    def __init__(self, ratings_data, titles_data, students_data, z_data, r_z_data):
        self.ratings = ratings_data
        self.titles = titles_data
        self.students = students_data
        self.movie_mean = dict()
        self.z_data = z_data
        self.r_z_data = r_z_data
        self.z_i = np.zeros((len(self.students[:,0]), len(self.z_data[:])))
        self.z_total = np.zeros(len(self.students[:,0]))
        self.p_it = np.zeros((len(self.students[:,0]), len(self.z_data[:])))
        self.l = 0.0

    def compute_mean(self):
        i = 0
        j = 0

        while i < len(self.titles[:,0]):
            go_watch = 0
            total = 0
            j = 0
            while j < len(self.students[:,0]):
                if self.ratings[j,i] == '1':
                    go_watch += 1
                if self.ratings[j,i] != '?':
                     total += 1
                j += 1
            mean = (1.0 * go_watch) / (1.0 * total)
            title = self.titles[i,0]
            self.movie_mean[title] = mean
            i += 1
        sorted_dict = sorted(self.movie_mean.items(), key=operator.itemgetter(1))
        i = 0
        while i < len(sorted_dict):
            print (str(sorted_dict[i]))
            i += 1

    def calculate_product(self, t):
        i = 0
        prob = 0.0
        total = 0.0

        while i < len(self.z_data[:]):
            product = 1.0
            j = 0
            while j < len(self.r_z_data[:,0]):
                ''' Need to check if rating is 0, 1 or ? '''
                if self.ratings[t,j] == '1' or self.ratings[t,j] == '0':
                    rating = int(self.ratings[t,j])
                    if rating == 1:
                        prob = float(self.r_z_data[j,i])
                    else:
                        prob = 1.0 - float(self.r_z_data[j,i])
                        ''' done with check '''
                    product *= prob
                j += 1
            ''' saving the numerator for the E step for each z_i and student t '''
            self.z_i[t,i] = (float(self.z_data[i]) * product)

            total += (float(self.z_data[i]) * product)
            i += 1
        ''' saving the denominator for the E step for all students '''
        self.z_total[t] = total
        return total

    def max_likelihood(self):
        t = 0
        total = 0.0
        prob = 0.0

        while t < len(self.students[:,0]):
            prob = self.calculate_product(t)
            l = math.log(prob)
            total += l
            t += 1
        total = total / len(self.students[:,0])
        self.l = total

    def E_step(self):
        t = 0

        while t < len(self.z_total[:]):
            i = 0
            while i < len(self.z_i[0,:]):
                self.p_it[t,i] = self.z_i[t,i] / self.z_total[t]
                i += 1
            t += 1

    def M_step(self):
        ''' first going to determine the r_z values '''
        total = 0.0
        p_total = 0.0
        j = 0

        while j < len(self.r_z_data[:,0]):
            i = 0
            while i < len(self.r_z_data[0,:]):
                t = 0
                total = 0.0
                p_total = 0.0
                while t < len(self.ratings[:,0]):
                    if (self.ratings[t,j] == '1') or (self.ratings[t,j] == '0'):
                        if int(self.ratings[t,j]) == 1:
                            total += self.p_it[t,i]
                    else:
                        total += (self.p_it[t,i] * float(self.r_z_data[j,i]))
                    p_total += self.p_it[t,i]
                    t += 1
                self.r_z_data[j,i] = total / p_total
                i += 1
            j += 1

        ''' second is deterine the z values '''
        col_sum = np.sum(self.p_it, axis=0)
        self.z_data = col_sum / len(self.p_it[:,0])


if __name__ == "__main__":
    ratings_file = open('hw5_movieRatings.txt', 'r')
    ratings_data = np.array([line.rstrip().split(" ") for line in ratings_file])
    ratings_file.close

    titles_file = open('hw5_movieTitles.txt', 'r')
    titles_data = np.array([line.rstrip().split(" ") for line in titles_file])
    titles_file.close

    students_file = open('hw5_studentPIDs.txt', 'r')
    students_data = np.array([line.rstrip().split(" ") for line in students_file])
    students_file.close

    probZ_file = open('hw5_probZ_init.txt', 'r')
    z_data = np.array([line.rstrip().split("    ") for line in probZ_file])
    z_data = z_data[:, 1]
    probZ_file.close

    probR_givenZ_file = open('hw5_probRgivenZ_init.txt', 'r')
    r_z_data = np.array([line.rstrip().split("   ") for line in probR_givenZ_file])
    r_z_data = r_z_data[:, 1:len(r_z_data[0,:])]
    probR_givenZ_file.close

    data = movieRatings(ratings_data, titles_data, students_data, z_data, r_z_data)

    data.compute_mean()
    total_count = 128
    print_set = set([0, 1, 2, 4, 8, 16, 32, 64])
    i = 0
    while i < total_count:
        data.max_likelihood()
        data.E_step()
        data.M_step()
        if i in print_set:
            print (str(i) + ':\t' + str(data.l))
        i += 1
    print (str(i) + ':\t' + str(data.l))

    my_dict = dict()

    index = 0
    while index < len(data.students[:,0]):
        if data.students[index,0] == 'A12409694':
            break
        index += 1

    t = 0
    while t < len(data.titles[:]):
        total = 0.0
        i = 0
        if data.ratings[index, t] == '?':
            while i < len(data.r_z_data[0,:]):
                total += (data.p_it[t, i] * float(data.r_z_data[t, i]))
                i += 1
            my_dict[str(data.titles[t])] = total
        t += 1

    sorted_dict = sorted(my_dict.items(), key=operator.itemgetter(1))
    i = 0
    while i < len(sorted_dict):
        print (str(sorted_dict[i]))
        i += 1

    i = 0 
