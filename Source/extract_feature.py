#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Forth step for RITE: extract feature of sentence pair"""

import text_pair
import re


MAX_EDIT_DISTANCE = 45.0


def extract_all_fea(text, text_cut, text_entity, text_lex):
    """
    get all the feature
    :param text: text_pair.TextPair class
    :return: list of feature
    """

    t1 = text.t1
    t2 = text.t2

    t1_cut = text_cut.t1.split()
    t2_cut = text_cut.t2.split()

    return [fea_quotation(t1, t2)]


def has_alpha(simple_text):
    """ judge str whether has english char"""

    for uchar in simple_text:
        if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
            return True

    return False


def n_gram_overlap(t1, t2):
    pass


def entailment_score(t1, t2):
    pass


def cosine_similarity(t1, t2):
    pass


def edit_distance_r(t1_cut, t2_cut):
    def edit_distance(_t1, _t2):
        m = len(_t1)
        n = len(_t2)

        d = [[0 for i in range(n + 1)] for j in range(m + 1)]

        for i in range(m):
            d[i][0] = i
        for j in range(n):
            d[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0

                if _t1[i - 1] == _t2[j - 1]:
                    cost = 0
                else:
                    cost = 1
                d[i][j] = min(d[i - 1][j] + 1,
                              d[i][j - 1] + 1,
                              d[i - 1][j - 1] + cost)
        return d[m][n]

    ratio = edit_distance(t1_cut, t2_cut) / MAX_EDIT_DISTANCE

    return min(1.0, ratio)


def lcs_overlap(t1, t2):
    pass


def tree_edit_distance_r(t1, t2):
    pass


def tree_parser_r(t1, t2):
    pass


def fea_longer(t1_cut, t2_cut):
    """whether length of t1 shorter than t2"""

    if len(t1_cut) < len(t2_cut):
        return 1

    return 0


def fea_longer4(t1_cut, t2_cut):
    """whether length of t1 shorter than t2 with length 4"""

    if len(t1_cut) + 4 < len(t2_cut):
        return 1

    return 0


def fea_part(t1, t2):
    pass


def fea_time_equal(t1, t2):
    pass


def fea_num_equal(t1, t2):
    pass


def fea_num(t1, t2):
    pass


def fea_english(t1, t2):
    """
    whether has english words together
    """
    if not has_alpha(t1) and has_alpha(t2):
        return 1

    return 0


def fea_bracket(t1, t2):
    pass


def fea_quotation(t1, t2):
    """whether the contents of t2 quotation marks are not in t1"""

    patten = re.compile(r'["“](.*?)["”]')
    quota_cont = re.findall(patten, t2)

    for ele in quota_cont:
        if ele not in t1:
            return 1

    return 0


def fea_allentity(t1, t2):
    pass


def fea_and(t1, t2):
    pass


def fea_or(t1, t2):
    pass


def fea_antonym(t1, t2):
    pass


def fea_synonym(t1, t2):
    pass


def fea_hyper_ud(t1, t2):
    pass


def fea_hyper_du(t1, t2):
    pass


def fea_neg(t1, t2):
    pass


def fea_wish(t1, t2):
    pass


def fea_may(t1, t2):
    pass


def fea_sum(t1, t2):
    pass


def fea_hrise(t1, t2):
    pass


def fea_hfall(t1, t2):
    pass


if __name__ == '__main__':
    text_all = text_pair.read_text('../Data/test.txt')
    text_cut_all = text_pair.read_text('../Data/test_cut.txt')

    if len(text_all) != len(text_cut_all):
        exit(-1)

    for i in range(len(text_all)):
        extract_all_fea(text_all[i], text_cut_all[i], 0, 0)
