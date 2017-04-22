#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""bigram model"""

import time
import copy
import numpy as np
from scipy.sparse import csr_matrix
from base_processing import *

MAX_DICT_LEN = 1000
MAX_WORD_LEN = 6
DEBUG = 0

# root path for model
root_path = '../Models/bigram/'


class Bigram():
    """
    Bigram language model
    """

    SINDEX = 0
    EINDEX = 1

    # word directory, initial for start and end
    words_dic = ['<s>', '</s>']

    # uni word count
    uni_cnt = np.zeros((MAX_DICT_LEN,), dtype=np.int32)

    # word pair count
    bi_cnt = np.zeros((MAX_DICT_LEN, MAX_DICT_LEN), dtype=np.int32)

    # discount values defined as Chen and Goodman from D1 to D3
    kn_d_cg98 = [0., 0., 0.]

    # different bigram number
    kn_diff_bi = 0

    # every rows: bi_cnt[index1][i] == 1, bi_cnt[index1][i] == 2, bi_cnt[index1][i] >= 3
    kn_diff_bi_row = np.zeros((3, MAX_DICT_LEN), dtype=np.int32)

    # every rows: bi_cnt[i][index2] >= 1
    kn_diff_bi_col = np.zeros((1, MAX_DICT_LEN), dtype=np.int32)

    @staticmethod
    def find_word_dic(word):
        """
        find word in bigram word dictionary or insert it
        :return: pos in dictionary
        """

        if len(Bigram.words_dic) >= MAX_DICT_LEN:
            return -1

        if word not in Bigram.words_dic:
            Bigram.words_dic.append(word)

        return Bigram.words_dic.index(word)

    @staticmethod
    def calc_prob(word1, word2):
        """
        calculate the bigram probability of word2/word1
        :return: probability in [0,1]
        """

        # OOV
        if word1 not in Bigram.words_dic or word2 not in Bigram.words_dic:
            return -1

        index1 = Bigram.words_dic.index(word1)
        index2 = Bigram.words_dic.index(word2)

        return Bigram._calc_prob_mod_kn(index1, index2)  # kn smoothing

    # not used
    @staticmethod
    def _calc_prob_add_one(index1, index2):
        """
        add one smoothing
        :return: probability in [0,1]
        """
        return (Bigram.bi_cnt[index1][index2] + 1) * 1.0 / Bigram.uni_cnt[index1]

    @staticmethod
    def _calc_prob_mod_kn(index1, index2):
        """
        Modified Kneser-Ney Smoothing, high speed but need the pre-training model
        :return: probability in [0,1]
        """

        # discount values
        def D(x):
            # x>0
            if x >= 3:
                return Bigram.kn_d_cg98[2]
            elif x == 0:
                return 0

            return Bigram.kn_d_cg98[x - 1]

        prob_high = max(Bigram.bi_cnt[index1][index2] - D(Bigram.bi_cnt[index1][index2]), 0) * 1. / Bigram.uni_cnt[
            index1]

        lamb = (Bigram.kn_d_cg98[0] * Bigram.kn_diff_bi_row[0][index1] + Bigram.kn_d_cg98[1] * Bigram.kn_diff_bi_row[1][
            index1]
                + Bigram.kn_d_cg98[2] * Bigram.kn_diff_bi_row[2][index1]) * 1. / Bigram.uni_cnt[index1]

        prop_low = Bigram.kn_diff_bi_col[0][index2] * 1. / Bigram.kn_diff_bi

        return prob_high + lamb * prop_low

    # not used
    @staticmethod
    def _calc_prob_mod_kn_slow(index1, index2):
        """
        Modified Kneser-Ney Smoothing, slower speed but more general
        :return: probability in [0,1]
        """

        # discount values
        def D(x):
            # x>0
            if x >= 3:
                return Bigram.kn_d_cg98[2]
            elif x == 0:
                return 0

            return Bigram.kn_d_cg98[x - 1]

        prob_high = max(Bigram.bi_cnt[index1][index2] - D(Bigram.bi_cnt[index1][index2]), 0) * 1. / Bigram.uni_cnt[
            index1]

        n = [0, 0, 0]
        for i in range(len(Bigram.words_dic)):
            if Bigram.bi_cnt[index1][i] == 1:
                n[0] += 1
            elif Bigram.bi_cnt[index1][i] == 2:
                n[1] += 1
            elif Bigram.bi_cnt[index1][i] >= 3:
                n[2] += 1

        lamb = (Bigram.kn_d_cg98[0] * n[0] + Bigram.kn_d_cg98[1] * n[1] + Bigram.kn_d_cg98[2] * n[2]) * 1. \
               / Bigram.uni_cnt[index1]

        temp_cnt = 0
        for i in range(len(Bigram.words_dic)):
            if Bigram.bi_cnt[i][index2] > 0:
                temp_cnt += 1
        prop_low = temp_cnt * 1. / Bigram.kn_diff_bi

        return prob_high + lamb * prop_low


def build_bi_gram_cnt(train_text):
    """
    count the uni word and word pair
    :param train_text: filename for train
    """

    def update_cnt(last_index, cur_index):
        Bigram.uni_cnt[cur_index] += 1
        Bigram.bi_cnt[last_index][cur_index] += 1

        # build kn arguments of different bigram in rows and cols
        if Bigram.bi_cnt[last_index][cur_index] == 1:
            Bigram.kn_diff_bi_row[0][last_index] += 1  # count for bi_cnt[index1][i] == 1

            Bigram.kn_diff_bi_col[0][cur_index] += 1  # count for bi_cnt[i][index2] >= 1

        elif Bigram.bi_cnt[last_index][cur_index] == 2:  # count for bi_cnt[index1][i] == 2
            Bigram.kn_diff_bi_row[1][last_index] += 1
            Bigram.kn_diff_bi_row[0][last_index] -= 1

        elif Bigram.bi_cnt[last_index][cur_index] == 3:  # count for bi_cnt[index1][i] >= 3
            Bigram.kn_diff_bi_row[2][last_index] += 1
            Bigram.kn_diff_bi_row[1][last_index] -= 1

    # precess lines to construct cnt table
    line_num = 0
    for line in train_text:
        lwords = TextParse.from_segment(line)

        # count the line start label '<s>'
        last_index = Bigram.SINDEX
        Bigram.uni_cnt[last_index] += 1

        # count the line words
        for word in lwords:
            cur_index = Bigram.find_word_dic(word)
            if cur_index == -1:
                continue

            update_cnt(last_index, cur_index)
            last_index = cur_index

        # count the line end label '</s>'
        cur_index = Bigram.EINDEX
        update_cnt(last_index, cur_index)

        # debug print
        line_num += 1
        if DEBUG and line_num % 100 == 0:
            print('line: ' + str(line_num))


def build_arg_cg98():
    """
    calculate the arguments of KN smoothing defined by Chen and Goodman
    """

    kn_n = [0, 0, 0, 0]

    points = Bigram.bi_cnt.nonzero()
    x = points[0]
    y = points[1]

    Bigram.kn_diff_bi = len(x)

    for i in range(len(x)):
        cx = x[i]
        cy = y[i]
        if 4 >= Bigram.bi_cnt[cx][cy] > 0:
            kn_n[Bigram.bi_cnt[cx][cy] - 1] += 1

    for i in range(4):
        if kn_n[i] == 0:
            return

    Y = kn_n[0] * 1. / (kn_n[0] + 2 * kn_n[1])
    Bigram.kn_d_cg98[0] = 1 - 2 * Y * kn_n[1] * 1. / kn_n[0]
    Bigram.kn_d_cg98[1] = 2 - 3 * Y * kn_n[2] * 1. / kn_n[1]
    Bigram.kn_d_cg98[2] = 3 - 4 * Y * kn_n[3] * 1. / kn_n[2]


def save_sparse_csr(filename, array):
    # note that .npz extension is added automatically
    np.savez(filename, data=array.data, indices=array.indices,
             indptr=array.indptr, shape=array.shape)


def load_sparse_csr(filename):
    # here we need to add .npz extension manually
    loader = np.load(filename + '.npz')
    return csr_matrix((loader['data'], loader['indices'], loader['indptr']),
                      shape=loader['shape'])


def save_model():
    word_dic = np.array(Bigram.words_dic)

    np.save(root_path + 'word_dic', word_dic)
    np.save(root_path + 'uni_cnt', Bigram.uni_cnt)
    np.savez(root_path + 'kn_arg', d=Bigram.kn_d_cg98, num=Bigram.kn_diff_bi,
             diff_col=Bigram.kn_diff_bi_col, diff_row=Bigram.kn_diff_bi_row)
    save_sparse_csr(root_path + 'bi_cnt', csr_matrix(Bigram.bi_cnt))


def load_model():
    word_dic = np.load(root_path + 'word_dic.npy')
    Bigram.words_dic = word_dic.tolist()

    temp = np.load(root_path + 'kn_arg.npz')
    Bigram.kn_d_cg98 = temp['d']
    Bigram.kn_diff_bi = temp['num']
    Bigram.kn_diff_bi_row = temp['diff_row']
    Bigram.kn_diff_bi_col = temp['diff_col']

    Bigram.uni_cnt = np.load(root_path + 'uni_cnt.npy')
    Bigram.bi_cnt = load_sparse_csr(root_path + 'bi_cnt').toarray()


def train(pairList):
    train_txt1 = [textPair.t1 for textPair in pairList]
    train_txt2 = [textPair.t2 for textPair in pairList]

    build_bi_gram_cnt(train_txt1+train_txt2)
    build_arg_cg98()
    save_model()


if __name__ == '__main__':
    pairList = text_pair.read_text('../Data/train_cut.txt')
    train(pairList)