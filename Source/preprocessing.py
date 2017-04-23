#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Second step for RITE: preprocess data"""

from text_pair import *
from knowledge import *


def _convert_time(text):
    return text


def _convert_num(text):
    return text


def _convert_char(text):
    """
    replace '两' and '双' to '二'
    """

    for i in range(len(Idiom.idiom_with_two1)):
        if Idiom.idiom_with_two1[i] in text:
            text = text.replace(Idiom.idiom_with_two1[i], '<%d>' % i)

    for i in range(len(Idiom.idiom_with_two2)):
        if Idiom.idiom_with_two2[i] in text:
            text = text.replace(Idiom.idiom_with_two2[i], '[%d]' % i)

    text = text.replace('两', '二').replace('双', '二')

    for i in range(len(Idiom.idiom_with_two1)):
        if '<%d>' % i in text:
            text = text.replace('<%d>' % i, Idiom.idiom_with_two1[i])

    for i in range(len(Idiom.idiom_with_two2)):
        if '[%d]' % i in text:
            text = text.replace('[%d]' % i, Idiom.idiom_with_two2[i])

    return text


def _convert_unit(text):
    return text


def preprocess(textPair):
    """
    preprocessing function for using
    """
    t1 = textPair.t1
    t2 = textPair.t2

    def _prepro(text):
        text_n = _convert_num(text)
        text_c = _convert_char(text_n)
        text_m = _convert_time(text_c)
        return _convert_unit(text_m)

    return TextPair(_prepro(t1), _prepro(t2), textPair.label)


if __name__ == '__main__':
    textPair = TextPair('两个 一双 半斤八两', '车位成为', 'Y')
    newText = preprocess(textPair)
    print(newText.t1, newText.t2, newText.label, sep='\n')
