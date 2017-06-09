# Michael Covarrubias
# PID#: A12409694

import numpy as np
import math
import operator

class hangman:
    def __init__(self, word_data):
        self.word_data = word_data
        self.incorrect_list = set()
        self.correct_list = dict()
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.word_prob = dict()
        self.letter_prob = dict()
        self.curr_words = set()

        i = 0
        total = 0
        while i < len(self.word_data[:, 0]):
            total += int(self.word_data[i, 1])
            i+=1

        i = 0
        while i < len(self.word_data[:, 0]):
            self.word_prob[self.word_data[i, 0]] = (1.0 * int(self.word_data[i, 1])) / total
            i+=1

    def determine_current_words(self):
        ''' takes all the words that cannot be chosen based on the
            incorrect guesses and the correct guesses
        '''
        pos = [0, 1, 2, 3, 4]
        i = 0
        while i < len(self.word_data[:, 0]):
            word = self.word_data[i, 0]
            remove = 1
            for l in self.incorrect_list:
                if l in word:
                    remove = 0
            for key in self.correct_list:
                if self.correct_list[key] != word[key]:
                    remove = 0

                pos.remove(key)
                for x in pos:
                    if self.correct_list[key] == word[x]:
                        remove = 0
                pos.append(key)

            if remove == 1:
                self.curr_words.add(word)
            i+=1

    def determine_denominator(self):
        ''' assuming that we have already filtered out all the words
            that cannot be chosen
        '''
        total_sum = 0

        for word in self.curr_words:
            total_sum += self.word_prob[word]
        return total_sum

    def determine_probs(self):
        i = 0
        posterior_prob = 0.0
        letter_total_prob = 0.0
        numerator = 0.0
        denominator = 0.0
        denominator = self.determine_denominator()

        for l in self.alphabet:
            for word in self.curr_words:
                if l in word:
                    numerator = self.word_prob[word]
                    posterior_prob = numerator / denominator
                    letter_total_prob += posterior_prob
            self.letter_prob[l] = letter_total_prob
            letter_total_prob = 0.0

    def best_next_guess(self):
        max_val = 0

        for key in self.letter_prob:
            if self.letter_prob[key] > max_val:
                max_val = self.letter_prob[key]
                index = key
        print("best next guess: " + index)
        print("with probability: " + str(max_val))

if __name__ == "__main__":

    word_file = open('hw2_word_counts_05.txt', 'r')
    word_data = np.array([line.rstrip().split(" ") for  line in word_file])
    word_file.close
    data = hangman(word_data)

    incorrect = raw_input('Enter incorrect guesses letters separated by spaces: ')
    incorrect_list = np.array([incorrect.rstrip().split(" ")])

    correct = raw_input('Enter correct guesses letter followed by postion e.g A 1: ')
    correct_list = np.array([correct.rstrip().split(" ")])

    i = 0
    while i < len(incorrect_list[0, :]):
        if incorrect_list[0,i] == '':
            i+=1
        else:
            data.incorrect_list.add(incorrect_list[0, i])
            data.alphabet.remove(incorrect_list[0, i])
            i+=1

    i = 0
    while i < (len(correct_list[0, :]) - 1):
        data.correct_list[int(correct_list[0, i+1])] = correct_list[0, i]
        data.alphabet.remove(correct_list[0, i])
        i+=2

    for letter in data.alphabet:
        data.letter_prob[letter] = 0.0

    data.determine_current_words()
    data.determine_probs()
    data.best_next_guess()

    sorted_x = sorted(data.word_prob.items(), key=operator.itemgetter(1))
    i = 0
    print("Least 10 Probabilities (in increasing order): ")
    while i < 10:
        print(sorted_x[i])
        i+=1
    i = len(sorted_x) - 10
    print("Max 10 Probabilities (in increasing order): ")
    while i < len(sorted_x):
        print(sorted_x[i])
        i+=1
