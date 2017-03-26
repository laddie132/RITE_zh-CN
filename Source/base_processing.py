#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Third step for RITE: sentence split and grammar analysis"""


import jieba
import text_pair


def split_word(textPair):
    jieba.setLogLevel('INFO')

    ger1 = jieba.cut(textPair.t1)
    ger2 = jieba.cut(textPair.t2)

    t1 = ' '.join(ger1)
    t2 = ' '.join(ger2)

    return text_pair.TextPair(t1, t2, textPair.label)


if __name__ == '__main__':
    pairList = text_pair.read_text('../Data/test.txt')
    splitPairList = [split_word(t) for t in pairList]
    text_pair.save_text('../Data/test_cut.txt', splitPairList)