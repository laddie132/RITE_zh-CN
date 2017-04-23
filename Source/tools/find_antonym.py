#!/usr/in/python
# -*- coding: utf-8 -*-

import urllib.request
import re

p = re.compile(r'<li><a target="_blank" href="https://www.chazidian.com/fanyici/(\S+?)/" title="\S+?>\1 -- (\S+?)</a> </li>')

antonym = []
num = 1

for i in range(50):
    url = 'https://www.chazidian.com/fanyici/%d.html' % (i+1)
    res = urllib.request.urlopen(url)

    html_str = res.read().decode('utf-8')
    result = re.findall(p, html_str)

    for ele in result:
        if len(ele) != 2:
            continue

        antonym.append(str(num) + ' ' + ele[0] + ' ' + ele[1] + '\n')
        num += 1

    print(url)

fp = open('../../Models/knowledge/反义词_chazidian_com.txt', 'w', encoding='utf-8')
fp.writelines(antonym)

