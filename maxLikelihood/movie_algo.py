# Michael Covarrubias
# PID#: A12409694
# Email: mdcovarr@ucsd.edu
import numpy as np
import math
import operator
import matplotlib.pyplot as plt

class movie_algo:
    def __init__(self, vocab_data, unigram_data, bigram_data):
        self.vocab_data = vocab_data
        self.unigram_data = unigram_data
        self.bigram_data = bigram_data
        self.unigram_prob_dict = dict()
        self.unigram_dict = dict()
        self.bigram_dict = dict()

        i = 0
        total = 0.0
        while i < len(vocab_data[:,0]):
            total += int(unigram_data[i, 0])
            self.unigram_dict[vocab_data[i, 0]] = int(unigram_data[i,0])
            i += 1

        i = 0
        while i < len(vocab_data[:,0]):
            self.unigram_prob_dict[vocab_data[i, 0]] = (1.0 * int(unigram_data[i, 0])) / total
            i += 1
        i = 0
        while i < len(bigram_data[:, 0]):
            keys = (vocab_data[int(bigram_data[i, 0]) - 1, 0], vocab_data[int(bigram_data[i, 1]) - 1, 0])
            self.bigram_dict[keys] = int(bigram_data[i, 2])
            i += 1

    def calculate_part_a(self):
        i = 0
        text_file = open('part_a.txt', 'w')

        while i < len(self.vocab_data[:, 0]):
            word = self.vocab_data[i, 0]
            if word[0] == 'M':
                text_file.write(word + "\t" + str(self.unigram_prob_dict[word]) + "\n")
            i += 1
        text_file.close

    def calculate_part_b(self):
        i = 0
        total = 0.0
        one_dict = dict()

        while i < len(self.vocab_data[:, 0]):
            if self.vocab_data[i, 0] == "ONE":
                index = i + 1
                break
            i += 1

        i = 0
        while i < len(self.bigram_data[:, 0]):
            if int(self.bigram_data[i, 0]) == index:
                prob = (1.0 * int(self.bigram_data[i, 2])) / int(self.unigram_data[index, 0])
                one_dict[self.vocab_data[int(self.bigram_data[i, 1])-1, 0]] = prob

            i += 1

        text_file = open('part_b.txt', 'w')
        sorted_x = sorted(one_dict.items(), key=operator.itemgetter(1))
        i = len(sorted_x) - 10

        while i < len(sorted_x):
            text_file.write(str(sorted_x[i]) + "\n")
            i+=1

        text_file.close


    def calculate_part_c(self, phrase_1):
        log_u = 0.0
        log_b = 0.0
        i = 0
        text_file = open('part_c.txt', 'w')
        text_file.write('Unigram Model Likelihood:\n')
        while i < len(phrase_1):
            word = phrase_1[i]
            log_u += math.log(self.unigram_prob_dict[word])
            i += 1
        text_file.write(str(log_u) + '\n')

        i = 0
        val = np.array(["<s>"])
        phrase_new = np.concatenate((val, phrase_1), axis=0)

        text_file.write('Bigram Model Likelihood:\n')
        while i < len(phrase_new) - 1:
            prev_word = phrase_new[i]
            word = phrase_new[i+1]
            keys = (prev_word, word)
            log_b += math.log((1.0 * self.bigram_dict[keys]) / self.unigram_dict[prev_word])
            i += 1
        text_file.write(str(log_b) + '\n')
        text_file.close

    def calculate_part_d(self, phrase_2):
        log_u = 0.0
        log_b = 0.0
        i = 0

        text_file = open('part_d.txt', 'w')
        text_file.write('Unigram Model Likelihood:\n')
        while i < len(phrase_2):
            word = phrase_2[i]
            log_u += math.log(self.unigram_prob_dict[word])
            i += 1
        text_file.write(str(log_u) + '\n')

        i = 0
        val = np.array(["<s>"])
        phrase_new = np.concatenate((val, phrase_2), axis=0)

        text_file.write('Bigram Model Likelihood:\n')
        while i < len(phrase_new) - 1:
            prev_word = phrase_new[i]
            word = phrase_new[i+1]
            keys = (prev_word, word)
            isKey = self.bigram_dict.get(keys)
            if isKey == None:
                text_file.write(str(keys) + '\n')
                log_b += math.log(0.0000000001)
            else:
                log_b += math.log((1.0 * self.bigram_dict[keys]) / self.unigram_dict[prev_word])
            i += 1
        text_file.write(str(log_b) + '\n')

    def calculate_part_e(self, phrase_2):
        max_val = -100.00
        log_m = 0.0
        p_m = 0.0
        i = 0
        x = 0.00
        x_list = []
        y_list = []
        val = np.array(["<s>"])
        phrase_new = np.concatenate((val, phrase_2), axis=0)
        while x <= 1.00:
            while i < len(phrase_new) - 1:
                prev_word = phrase_new[i]
                word = phrase_new[i+1]
                keys = (prev_word, word)
                isKey = self.bigram_dict.get(keys)

                if isKey == None:
                    bigram_val = 0.0
                else:
                    bigram_val = (1.0 * self.bigram_dict[keys]) / self.unigram_dict[prev_word]

                unigram_val = self.unigram_prob_dict[word]
                p_m = ((1.0 - x) * unigram_val) + (x * bigram_val)
                log_m += math.log(p_m)
                i += 1

            x_list.append(x)
            y_list.append(log_m)

            if log_m > max_val:
                max_val = log_m
                max_lambda = x
            log_m = 0.0
            i = 0
            x += 0.01
        plt.plot(x_list, y_list)
        plt.show()
        print max_val
        print max_lambda

if __name__ == "__main__":

    vocab_file = open('vocab.txt', 'r')
    vocab_data = np.array([line.rstrip().split(" ") for line in vocab_file])
    vocab_file.close

    unigram_file = open('unigram.txt', 'r')
    unigram_data = np.array([line.rstrip().split(" ") for line in unigram_file])
    unigram_file.close

    bigram_file = open('bigram.txt', 'r')
    bigram_data = np.array([line.rstrip().split("\t") for line in bigram_file])
    bigram_file.close

    string_1 = "THE MARKET FELL BY ONE HUNDRED POINTS LAST WEEK"
    string_2 = "THE FOURTEEN OFFICIALS SOLD FIRE INSURANCE"
    phrase_1 = np.array(string_1.rstrip().split(" "))
    phrase_2 = np.array(string_2.rstrip().split(" "))

    data = movie_algo(vocab_data, unigram_data, bigram_data)
    data.calculate_part_a()
    data.calculate_part_b()
    data.calculate_part_c(phrase_1)
    data.calculate_part_d(phrase_2)
    data.calculate_part_e(phrase_2)
