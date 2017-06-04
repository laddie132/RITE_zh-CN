# -*- coding: utf-8 -*-

# Here are tools for the project

from text_pair import *
from convert_xml import *


def prepare_text(nlpcore, file_prefix):
    """
    prepare the train and test txt for speed
    """

    print("converting...")
    convert_to('../Data/' + file_prefix + '.xml', '../Data/' + file_prefix + '.txt')

    print("spliting...")
    tpair = read_text('../Data/' + file_prefix + '.txt')
    split_tpair = [nlpcore.split_sent_jieba(t) for t in tpair]
    save_text('../Data/' + file_prefix + '_cut.txt', split_tpair)

    print("pos_tagging...")
    pos_tpair = nlpcore.pos_tag_pairs(split_tpair)
    save_text('../Data/' + file_prefix + '_pos.txt', pos_tpair)

    print("ner_taging...")
    ner_tpair = nlpcore.ner_tag_pairs(split_tpair)
    save_text('../Data/' + file_prefix + '_ner.txt', ner_tpair)
    print("finished")


def merge_text(file1_prefix, file2_prefix, out_prefix):
    """
    merge two file to one
    """
    t1pair = read_text('../Data/' + file1_prefix + '.txt')
    t2pair = read_text('../Data/' + file2_prefix + '.txt')
    save_text('../Data/' + out_prefix + '.txt', t1pair + t2pair)
    print("finished")


def evaluate(initial_label, result_label):
    cnt_yn = [[0, 0], [0, 0]]

    for i in range(len(initial_label)):
        if initial_label[i] == 'Y' and result_label[i] == 'Y':
            cnt_yn[0][0] += 1
        elif initial_label[i] == 'Y' and result_label[i] == 'N':
            cnt_yn[0][1] += 1
        elif initial_label[i] == 'N' and result_label[i] == 'Y':
            cnt_yn[1][0] += 1
        elif initial_label[i] == 'N' and result_label[i] == 'N':
            cnt_yn[1][1] += 1

    py = cnt_yn[0][0] / (cnt_yn[0][0] + cnt_yn[1][0])
    pn = cnt_yn[1][1] / (cnt_yn[1][1] + cnt_yn[0][1])
    ry = cnt_yn[0][0] / (cnt_yn[0][0] + cnt_yn[0][1])
    rn = cnt_yn[1][1] / (cnt_yn[1][1] + cnt_yn[1][0])

    f1y = 2 * py * ry / (py + ry)
    f1n = 2 * pn * rn / (pn + rn)

    f1 = (f1y + f1n) / 2
    acc = (cnt_yn[0][0] + cnt_yn[1][1]) / (cnt_yn[0][0] + cnt_yn[0][1] + cnt_yn[1][0] + cnt_yn[1][1])

    return acc, f1
