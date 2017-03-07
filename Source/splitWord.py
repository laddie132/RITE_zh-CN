# -*- coding: utf-8 -*-

import jieba

jieba.setLogLevel('INFO')

test_str1 = '历史上没有乞力马札罗山火山喷发的记录。'
test_str2 = '历史上没有吉力马札罗火山喷发的记录。'
out_ger1 = jieba.lcut(test_str1)
out_ger2 = jieba.lcut(test_str2)

print('str1: ', '/'.join(out_ger1))
print('str2: ', '/'.join(out_ger2))