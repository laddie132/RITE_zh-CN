#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Forth step for RITE: extract feature of sentence pair"""

import math
import text_pair
import re
from bigram import *
from base_processing import *
from knowledge import *

MAX_EDIT_DISTANCE = 45.0
MAX_ANTONYM_NUM = 4
MAX_SYNONYM_NUM = 20


class TextFeature:
    """
    get all the feature
    """

    def __init__(self, text, text_cut, text_pos, text_ner, text_lex):
        self.t1 = text.t1
        self.t2 = text.t2

        self.t1_cut = TextParse.from_segment(text_cut.t1)
        self.t2_cut = TextParse.from_segment(text_cut.t2)

        self.t1_pos = TextParse.from_pos(text_pos.t1)
        self.t2_pos = TextParse.from_pos(text_pos.t2)

        self.t1_ner = TextParse.from_ner(text_ner.t1)
        self.t2_ner = TextParse.from_ner(text_ner.t2)

        self.feature = [self._n_gram_overlap(), self._entailment_score(), self._cosine_similarity(),
                        self._edit_distance_r(), self._lcs_overlap(), self._tree_edit_distance_r(),
                        self._tree_parser_r(), self._fea_longer(), self._fea_part(), self._fea_time_equal(),
                        self._fea_num_equal(),self._fea_num(), self._fea_english(), self._fea_bracket(),
                        self._fea_quotation(), self._fea_entity_name(), self._fea_entity_type(), self._fea_and(),
                        self._fea_or(), self._fea_antonym_ratio(), self._fea_synonym_ratio(), self._fea_hyper_ud(),
                        self._fea_hyper_du(), self._fea_neg(), self._fea_may()]

    def _n_gram_overlap(self):
        """
        bigram overlap
        """
        # generate pair of words for bigram
        def _create_bi(text_cut):
            text_cut.append('</s>')

            text_bi = []
            last_word = '<s>'

            for word in text_cut:
                text_bi.append((last_word, word))
                last_word = word

            return text_bi

        t1_bi = _create_bi(self.t1_cut)
        t2_bi = _create_bi(self.t2_cut)

        prop_comm = 0.
        prop_t2 = 0.
        for word_bi in t2_bi:
            prop = Bigram.calc_prob(word_bi[0], word_bi[1])
            prop_t2 += prop

            if word_bi in t1_bi:
                prop_comm += prop

        return prop_comm / prop_t2

    def _entailment_score(self):
        pow_ratio = 3
        idf_oov = 0.2

        idf_comm = 0.
        idf_t2 = 0.

        for word in self.t2_cut:
            idf = 0.

            if word not in Bigram.words_dic:      # OOV
                idf = idf_oov
            else:
                word_arg = Bigram.words_dic.index(word)
                idf = math.log(sum(Bigram.uni_cnt) * 1. / Bigram.uni_cnt[word_arg] + 0.01)

            idf = math.pow(idf, pow_ratio)      # highlight the proportion of different word
            idf_t2 += idf
            if word in self.t1_cut:
                idf_comm += idf

        return idf_comm / idf_t2

    def _cosine_similarity(self):
        words = []

        # add word to word list
        for word in self.t1_cut:
            if word not in words:
                words.append(word)
        for word in self.t2_cut:
            if word not in words:
                words.append(word)

        # calculate vector
        vec1 = [0 for i in range(len(words))]
        vec2 = [0 for i in range(len(words))]

        for word in self.t1_cut:
            idx = words.index(word)
            vec1[idx] += 1
        for word in self.t2_cut:
            idx = words.index(word)
            vec2[idx] += 1

        def _cos(vector1, vector2):
            dot_product = 0.0
            normA = 0.0
            normB = 0.0
            for a, b in zip(vector1, vector2):
                dot_product += a * b
                normA += a ** 2
                normB += b ** 2
            if normA == 0.0 or normB == 0.0:
                return None
            else:
                return dot_product / ((normA * normB) ** 0.5)

        return _cos(vec1, vec2)

    def _edit_distance_r(self):
        def _edit_distance(_t1, _t2):
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

        ratio = _edit_distance(self.t1_cut, self.t2_cut) / MAX_EDIT_DISTANCE

        return min(1.0, ratio)

    def _lcs_overlap(self):
        """
        The longest common sub - sequence similarity
        """
        def _lcs_len(a, b):
            lena = len(a)
            lenb = len(b)
            c = [[0 for i in range(lenb + 1)] for j in range(lena + 1)]
            for i in range(lena):
                for j in range(lenb):
                    if a[i] == b[j]:
                        c[i + 1][j + 1] = c[i][j] + 1
                    elif c[i + 1][j] > c[i][j + 1]:
                        c[i + 1][j + 1] = c[i + 1][j]
                    else:
                        c[i + 1][j + 1] = c[i][j + 1]
            return c[lena][lenb]

        return _lcs_len(self.t1_cut, self.t2_cut) * 1. / len(self.t2_cut)

    def _tree_edit_distance_r(self):
        return 1

    def _tree_parser_r(self):
        return 1

    def _fea_longer(self):
        """whether length of t1 shorter than t2"""

        if len(self.t1_cut) < len(self.t2_cut):
            return 1

        return 0

    def _fea_part(self):
        """
        whether t2 is part of t1 
        """

        sym = ['，', ',', ';', '；', '。']

        if self.t2 in self.t1:
            pos = self.t1.index(self.t2)
            sym_pos = pos + len(self.t2)
            if sym_pos < len(self.t1) and self.t1[sym_pos] in sym:
                return 1

        return 0

    def _fea_time_equal(self):
        """
        whether has same time
        """

        patten_year = re.compile(r'\d\d\d\d-\d\d-\d\d')
        patten_hour = re.compile(r'\d\d:\d\d:\d\d')

        for year in re.findall(patten_year, self.t2):
            if year not in self.t1:
                return 0

        for hour in re.findall(patten_hour, self.t2):
            if hour not in self.t1:
                return 0

        return 1

    def _fea_num_equal(self):
        """
        whether has same number
        """

        patten = re.compile(r'\d+')

        for num in re.findall(patten, self.t2):
            if num not in self.t1:
                return 0

        return 1

    def _fea_num(self):
        """
        whether has number together
        """

        def has_num(simple_text):
            """ judge str whether has number"""
            for uchar in simple_text:
                if uchar.isdigit():
                    return True

            return False

        if not has_num(self.t1) and has_num(self.t2):
            return 0

        return 1

    def _fea_english(self):
        """
        whether has english words together
        """

        def has_alpha(simple_text):
            """ judge str whether has english char"""

            for uchar in simple_text:
                if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
                    return True

            return False

        if not has_alpha(self.t1) and has_alpha(self.t2):
            return 0

        return 1

    def _fea_bracket(self):
        """
        whether bracket`s contents in t2 are not in t1
        """

        patten = re.compile(r'\[(.+?)\]|\((.+?)\)|【(.+?)】|（(.+?)）|{(.+?)}|\<(.+?)\>|〔(.+?)〕|《(.+?)》')
        bracket_cont_t = re.findall(patten, self.t2)

        def str_in_tuple(tu):
            for i in range(len(tu)):
                if tu[i] is not '':
                    return tu[i]

            return ''

        bracket_cont = [str_in_tuple(tu) for tu in bracket_cont_t]

        for ele in bracket_cont:
            if ele not in self.t1:
                return 0

        return 1

    def _fea_quotation(self):
        """whether the contents of t2 quotation marks are not in t1"""

        patten = re.compile(r'["“](.*?)["”]')
        quota_cont = re.findall(patten, self.t2)

        for ele in quota_cont:
            if ele not in self.t1:
                return 0

        return 1

    # TODO, need optimization
    def _fea_entity_name(self):
        """
        whether t1 and t2 has the same name entity
        """
        for word in self.t2_ner:
            if word[1] is not 'O':
                if word not in self.t1_ner:
                    return 0

        return 1

    def _fea_entity_type(self):
        """
        whether t1 and t2 has the same type entity
        """
        for word in self.t2_ner:
            if word[1] is not 'O':
                if word[1] not in [ele[1] for ele in self.t1_ner]:
                    return 0

        return 1

    def _fea_and(self):
        """
        whether t1 and t2 has '和' together
        """
        word_and = ['和', '与', '并', '且', '及']

        flag1 = False
        flag2 = False
        for word in word_and:
            if word in self.t1:
                flag1 = True

        for word in word_and:
            if word in self.t2:
                flag2 = True

        if not flag1 and flag2:
            return 0

        return 1

    def _fea_or(self):
        """
        whether t1 and t2 has '或' together
        """

        word_or = ['或']

        flag1 = False
        flag2 = False
        for word in word_or:
            if word in self.t1:
                flag1 = True

        for word in word_or:
            if word in self.t2:
                flag2 = True

        if not flag1 and flag2:
            return 0

        return 1

    # TODO: optimization
    def _fea_antonym_ratio(self):
        """
        antonym number ratio
        """
        return 0
        num = 0
        for word2 in self.t2_pos:
            for word1 in self.t1_pos:
                if word2[1] == word1[1]:
                    if Antonyms.judge_antonym(word2, word1):
                        num += 1
                        break

        return min(num * 1. / MAX_ANTONYM_NUM, 1)

    # TODO: optimization
    def _fea_synonym_ratio(self):
        """
        synonym number ratio
        """
        return 0
        num = 0
        for word2 in self.t2_pos:
            for word1 in self.t1_pos:
                if word1[1] == word2[1]:
                    if Synonyms.judge_synonyms(word2, word1):
                        num += 1
                        break

        return min(num * 1. / MAX_SYNONYM_NUM, 1)

    def _fea_hyper_ud(self):
        return 1

    def _fea_hyper_du(self):
        return 1

    def _fea_neg(self):
        """
        whether have negative word
        """
        word_neg = ['不是', '不可', '没有', '不要', '不能', '不得', '不让', '不应该' ,'否定', '并非', '禁止']

        flag_t1 = False
        flag_t2 = False

        for word in self.t2_cut:
            if word in word_neg:
                flag_t2 = True
        for word in self.t1_cut:
            if word in word_neg:
                flag_t1 = True

        if flag_t1 is not flag_t2:
            return 0

        return 1

    def _fea_may(self):
        """
        whether have different words express possible
        """
        word_may = ['可能', '好像', '或者', '大约', '粗略', '概略', '大体', '大致', '不定',
                    '大致', '大抵', '或许', '约略', '简略', '八成', '大要', '也许',
                    '大略', '不一定']
        word_must = ['一定', '肯定', '必须', '必需', '必然', '确定', '注定', '必定', '详细',
                     '确乎', '周密', '细致', '具体', '不会']

        def _judge(text, wordl):
            for word in text:
                if word in wordl:
                    return True
            return False

        flag_t1_may = _judge(self.t1_cut, word_may)
        flag_t1_must = _judge(self.t1_cut, word_must)
        flag_t2_may = _judge(self.t2_cut, word_may)
        flag_t2_must = _judge(self.t2_cut, word_must)

        if flag_t1_may is not flag_t2_may or flag_t1_must is not flag_t2_must:
            return 0

        return 1


if __name__ == '__main__':
    load_model()
    load_knowedge()

    text_all = text_pair.read_text('../Data/train.txt')
    text_cut_all = text_pair.read_text('../Data/train_cut.txt')
    text_pos_all = text_pair.read_text('../Data/train_pos.txt')
    text_ner_all = text_pair.read_text('../Data/train_ner.txt')

    for i in range(len(text_all)):
        t = TextFeature(text_all[i], text_cut_all[i], text_pos_all[i], text_ner_all[i], 0).feature
        print(t[19])

    # fea = fea_bracket('14策1925-10-00委1925-10-15，会ewfewfew 05:10:00', '14策(策)-（10）-【0】0委1《92》5-<1>0-1{5}')
    # print(fea)
