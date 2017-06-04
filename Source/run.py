#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""run script for RITE"""

import bigram
import utils
from extract_feature import *
from base_processing import *
from preprocessing import *
from knowledge import *
from sklearn import svm
from sklearn.externals import joblib


# contruct nlp model
nlpcore = NLPCore()

# load knowedge library
load_knowedge()


def core(tpair):
    """
    core function for test a pair of text
    :return: text feature vector
    """

    # preprocessing
    tpair = preprocess(tpair)

    # base processing
    tpair_cut = nlpcore.split_sent_jieba(tpair)
    tpair_pos = nlpcore.pos_tag(tpair_cut)
    tpair_ner = nlpcore.ner_tag(tpair_cut)
    tpair_dep = nlpcore.depen_parse(tpair_cut)

    # extract feature
    tfeature = TextFeature(tpair, tpair_cut, tpair_pos, tpair_ner, tpair_dep)
    return tfeature.feature


def train(gamma=0.):
    vec = []
    label = []

    train_all = text_pair.read_text('../Data/train.txt')
    train_cut_all = text_pair.read_text('../Data/train_cut.txt')
    train_pos_all = text_pair.read_text('../Data/train_pos.txt')
    train_ner_all = text_pair.read_text('../Data/train_ner.txt')

    bigram.train(train_cut_all)

    print("extracting feature...")
    for i in range(len(train_all)):
        tfea = TextFeature(train_all[i], train_cut_all[i], train_pos_all[i], train_ner_all[i], 0)
        vec.append(tfea.feature)
        label.append(train_all[i].label)

        if i % 10 == 0:
            print(" cur: ", i)

    print("training...")
    # training
    if gamma:
        clf = svm.SVC(gamma=gamma)
    else:
        clf = svm.SVC()
    clf.fit(vec, label)

    # reserve
    joblib.dump(clf, '../Models/svm_model.m')

    result = clf.predict(vec)
    acc, f1 = utils.evaluate(label, result)
    print("Accuracy: ", acc)
    print("macroF1: ", f1)


def test(SHOW=1):
    clf = joblib.load('../Models/svm_model.m')
    bigram.load_model()

    if not SHOW:
        vec = []

        test_all = text_pair.read_text('../Data/test.txt')
        test_cut_all = text_pair.read_text('../Data/test_cut.txt')
        test_pos_all = text_pair.read_text('../Data/test_pos.txt')
        test_ner_all = text_pair.read_text('../Data/test_ner.txt')

        print("extracting feature...")
        for i in range(len(test_all)):
            tfea = TextFeature(test_all[i], test_cut_all[i], test_pos_all[i], test_ner_all[i], 0)
            vec.append(tfea.feature)

            if i % 10 == 0:
                print(" cur: ", i)

        result = clf.predict(vec)
        label = [ele.label for ele in test_all]

        acc, f1 = utils.evaluate(label, result)
        print("Accuracy: ", acc)
        print("macroF1: ", f1)

    else:

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
    # prepare_text('test')
    # prepare_text('train')

    # merge_text("train3", "train2", "train")
    # merge_text("train3_cut", "train2_cut", "train_cut")
    # merge_text("train3_pos", "train2_pos", "train_pos")
    # merge_text("train3_ner", "train2_ner", "train_ner")

    # train(0.4)
    test(SHOW=0)

    # for gamma in range(4, 5):
    #     print(gamma / 10.0, end=' ')
    #     train(gamma / 10.0)
    #     main(SHOW=0)
