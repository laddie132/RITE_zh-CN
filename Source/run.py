#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""run script for RITE"""

import bigram
from text_pair import *
from convert_xml import *
from extract_feature import *
from base_processing import *
from preprocessing import *
from sklearn import svm
from sklearn.externals import joblib


# contruct nlp model
nlpcore = NLPCore()


def prepare_text():
    """
    prepare all the train and test txt for speed
    """

    # train-xml-file
    convert_to('../Data/train.xml', '../Data/train.txt')

    train_pair = text_pair.read_text('../Data/train.txt')
    split_train_pair = [nlpcore.split_word_jieba(t) for t in train_pair]
    text_pair.save_text('../Data/train_cut.txt', split_train_pair)

    pos_train_pair = [nlpcore.pos_tag(t) for t in split_train_pair]
    text_pair.save_text('../Data/train_pos.txt', pos_train_pair)

    ner_train_pair = [nlpcore.ner_tag(t) for t in split_train_pair]
    text_pair.save_text('../Data/train_ner.txt', ner_train_pair)

    # test-xml-file
    convert_to('../Data/test.xml', '../Data/test.txt')

    test_pair = text_pair.read_text('../Data/test.txt')
    split_test_pair = [nlpcore.split_word_jieba(t) for t in test_pair]
    text_pair.save_text('../Data/test_cut.txt', split_test_pair)

    pos_test_pair = [nlpcore.pos_tag(t) for t in split_test_pair]
    text_pair.save_text('../Data/test_pos.txt', pos_test_pair)

    ner_test_pair = [nlpcore.ner_tag(t) for t in split_test_pair]
    text_pair.save_text('../Data/test_ner.txt', ner_test_pair)


def core(tpair):
    """
    core function for rite
    :return: text feature vector
    """

    # preprocessing
    tpair = preprocess(tpair)

    # base processing
    tpair_cut = nlpcore.split_word_jieba(tpair)
    tpair_pos = nlpcore.pos_tag(tpair)
    tpair_ner = nlpcore.ner_tag(tpair)
    tpair_dep = nlpcore.depen_parse(tpair)

    # extract feature
    tfeature = TextFeature(tpair, tpair_cut, tpair_pos, tpair_ner, tpair_dep)
    return tfeature.feature


def main(TRAIN=0, TEST=0, SHOW=1):

    if TRAIN:
        vec = []
        label = []

        train_all = text_pair.read_text('../Data/train.txt')
        train_cut_all = text_pair.read_text('../Data/train_cut.txt')
        train_pos_all = text_pair.read_text('../Data/train_pos.txt')
        train_ner_all = text_pair.read_text('../Data/train_ner.txt')

        bigram.train(train_cut_all)

        for i in range(len(train_all)):
            tfea = TextFeature(train_all[i], train_cut_all[i], train_pos_all[i], train_ner_all[i], 0)
            vec.append(tfea.feature)
            label.append(train_all[i].label)

        # training
        clf = svm.SVC()
        clf.fit(vec, label)

        # reserve
        joblib.dump(clf, '../Models/svm_model.m')

        result = clf.predict(vec)
        print("Result: ", result)

    else:
        clf = joblib.load('../Models/svm_model.m')
        bigram.load_model()

        if TEST:
            vec = []

            test_all = text_pair.read_text('../Data/test.txt')
            test_cut_all = text_pair.read_text('../Data/test_cut.txt')
            test_pos_all = text_pair.read_text('../Data/test_pos.txt')
            test_ner_all = text_pair.read_text('../Data/test_ner.txt')

            for i in range(len(test_all)):
                tfea = TextFeature(test_all[i], test_cut_all[i], test_pos_all[i], test_ner_all[i], 0)
                vec.append(tfea.feature)

            label = clf.predict(vec)
            result = [label[i] == test_all[i].label for i in range(len(label))]

            num = 0
            for ele in result:
                if ele:
                   num += 1

            print("Result: ", num * 1. / len(result))

        elif SHOW:

            # contruct text pair
            t1 = input("text1: ")
            t2 = input("text2: ")
            tpair = TextPair(t1, t2)

            # get feature
            vec = core(tpair)

            # svm classfier
            result = clf.predict([vec])
            print("Result: ", result)


if __name__ == '__main__':
    # prepare_text()

    main(1, 1, 0)
