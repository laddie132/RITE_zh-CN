#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Third step for RITE: sentence split and grammar analysis"""

import jieba
import text_pair
from nltk.tag import StanfordNERTagger
from nltk.tag import StanfordPOSTagger
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize.stanford_segmenter import StanfordSegmenter

DEBUG = 0


class NLPCore:
    """
    nlp processing including Stanford Word Segmenter, Stanford POS Tagger, 
    Stanford Named Entity Recognizer and Stanford Parser 
    """

    def __init__(self):
        self.root_path = '../Models/stanfordNLP/'

        # word segmenter
        self.segmenter = StanfordSegmenter(
            path_to_jar=self.root_path + "stanford-segmenter.jar",
            path_to_slf4j=self.root_path + "log4j-over-slf4j.jar",
            path_to_sihan_corpora_dict=self.root_path + "segmenter/",
            path_to_model=self.root_path + "segmenter/pku.gz",
            path_to_dict=self.root_path + "segmenter/dict-chris6.ser.gz")

        # pos tagger
        self.posTagger = StanfordPOSTagger(self.root_path + 'pos-tagger/chinese-distsim.tagger',
                                           path_to_jar=self.root_path + "stanford-postagger.jar")

        # named entity recognizer
        self.nerTagger = StanfordNERTagger(self.root_path + 'ner/chinese.misc.distsim.crf.ser.gz',
                                           path_to_jar=self.root_path + 'stanford-ner.jar')

        self.parser = StanfordDependencyParser(model_path=self.root_path + 'lexparser/chinesePCFG.ser.gz',
                                               path_to_jar=self.root_path + 'stanford-parser.jar',
                                               path_to_models_jar=self.root_path + 'stanford-parser-3.7.0-models.jar',
                                               encoding='gbk')

    def split_word_stanford(self, textPair):
        """
        Stanford Word Segmenter, input should be raw text
        :return: also TextPair with raw string of results
        """
        t1 = self.segmenter.segment(textPair.t1)
        t2 = self.segmenter.segment(textPair.t1)

        if DEBUG:
            print(t1, t2)

        return text_pair.TextPair(t1, t2, textPair.label)

    def split_word_jieba(self, textPair):

        jieba.setLogLevel('INFO')
        ger1 = jieba.cut(textPair.t1)
        ger2 = jieba.cut(textPair.t2)

        t1 = ' '.join(ger1)
        t2 = ' '.join(ger2)

        return text_pair.TextPair(t1, t2, textPair.label)

    def pos_tag(self, textPair):
        """
        Stanford POS Tagger, input should be splitted
        :return: also TextPair with raw string of results
        """
        t1_s = textPair.t1.split()
        t2_s = textPair.t2.split()

        t1_tag = ' '.join([ele[1] for ele in self.posTagger.tag(t1_s)])
        t2_tag = ' '.join([ele[1] for ele in self.posTagger.tag(t2_s)])

        if DEBUG:
            print(t1_tag, t2_tag)

        return text_pair.TextPair(t1_tag, t2_tag, textPair.label)

    def ner_tag(self, textPair):
        """
        Stanford Named Entity Recognizer, input should be splitted
        :return: also TextPair with raw string of results
        """
        t1_s = textPair.t1.split()
        t2_s = textPair.t2.split()

        t1_ner = ' '.join([ele[0] + '#' + ele[1] for ele in self.nerTagger.tag(t1_s)])
        t2_ner = ' '.join([ele[0] + '#' + ele[1] for ele in self.nerTagger.tag(t2_s)])

        if DEBUG:
            print(t1_ner, t2_ner)

        return text_pair.TextPair(t1_ner, t2_ner, textPair.label)

    def depen_parse(self, textPair):
        """
        Stanford Dependency Parser, input should be splitted
        :return: also TextPair with raw string of results
        """
        print([p.tree() for p in self.parser.raw_parse(textPair.t1)])
        # print(list(self.parser.parse(textPair.t1.split())))


class TextParse:

    def __init__(self):
        pass

    @staticmethod
    def from_segment(tsegment):
        return tsegment.split()

    @staticmethod
    def from_pos(tpos):
        return [ele.split('#') for ele in tpos.split()]

    @staticmethod
    def from_ner(tner):
        return [ele.split('#') for ele in tner.split()]

    @staticmethod
    def from_dep(tdep):
        pass


if __name__ == '__main__':
    nlpcore = NLPCore()

    pairList = text_pair.read_text('../Data/test_cut.txt')
    splitPairList = [nlpcore.ner_tag(t) for t in pairList]
    # text_pair.save_text('../Data/test_ner.txt', splitPairList)
