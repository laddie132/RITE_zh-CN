#!/usr/bin/python3
# -*- coding: utf-8 -*-

import jieba
import text_pair

def splitWord(textPair):
    jieba.setLogLevel('INFO')

    ger1 = jieba.cut(textPair.t1)
    ger2 = jieba.cut(textPair.t2)

    t1 = ' '.join(ger1)
    t2 = ' '.join(ger2)

    return text_pair.TextPair(t1, t2, textPair.label)

if __name__ == '__main__':
    pairList = text_pair.readFromText('../Data/train.txt')
    splitPairList = [splitWord(t) for t in pairList]
    text_pair.saveToText('../Data/train_cut.txt', splitPairList)