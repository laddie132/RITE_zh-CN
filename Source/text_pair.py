#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Data structure for RITE: description of text pair"""


class TextPair:
    """
    a pair of text for RITE
    """

    def __init__(self, t1='', t2='', label=''):
        self.t1 = t1
        self.t2 = t2
        self.label = label


def readFromText(fileName):
    f = open(fileName, encoding='utf-8')
    lines = f.readlines()
    pairs = int(len(lines) / 3)
    pairList = []

    for i in range(pairs):
        lineT1 = lines[3 * i].strip('\n')
        lineT2 = lines[3 * i + 1].strip('\n')
        lineLabel = lines[3 * i + 2].strip('\n')

        i1 = lineT1.index(' ')
        i2 = lineT2.index(' ')

        textPair = TextPair()
        textPair.t1 = lineT1[i1:]
        textPair.t2 = lineT2[i2:]
        textPair.label = lineLabel[0]

        pairList.append(textPair)

    return pairList


def saveToText(filename, pairList):
    f = open(filename, 'w', encoding='utf-8')
    for i in range(len(pairList)):
        f.write(str(i*3) + ' ' + pairList[i].t1 + '\n')
        f.write(str(i*3 + 1) + ' ' + pairList[i].t2 + '\n')
        f.write(pairList[i].label + '\n')

    f.close()
