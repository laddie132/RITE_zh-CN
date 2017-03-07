#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

def findIdiom(htmlName):
    """
    find any idiom in html file
    :param htmlName: html file path
    :return: idiom list
    """

    f = open(htmlName, encoding='utf-8')

    patten = re.compile(r'<u>(.*?)</u>')

    idiomList = patten.findall(f.read())
    idiomList = [s.strip() for s in idiomList]

    f.close()
    return idiomList


if __name__ == '__main__':
    idiomList = findIdiom('idiom_two2.html')
    print(idiomList)