
import numpy as np
import math
import sys
import argparse
import json
import html
import requests
import os
from bs4 import BeautifulSoup
import glob
import pandas as pd
import urllib.parse
import copy

soup = BeautifulSoup(open('data/異体字リスト _ 東文研　総合検索.html'), "html.parser")

print(str(soup))

trs = soup.find_all("tr")

map = {}

dd = {}

lines = []

for tr in trs:
    tds = tr.find_all("td")

    if len(tds) != 2:
        continue

    # print(tds)

    key = tds[0].text.strip()
    vars = tds[1].text.replace("　", " ").split(" ")

    line = set({key})

    for v in vars:
        v = v.strip()
        line.add(v)

    lines.append(line)

    '''
    if len(lines) > 2000:
        break
    '''

lines2 = []
for line in lines:
    flg = False
    index = -1

    for i in range(len(lines2)):
        line2 = lines2[i]
        for e in line:
            if e in line2:
                flg = True
                # line_target = line2
                index = i

                break

    if flg:
        for e in line:
            lines2[index].add(e)

    else:
        lines2.append(line)

lines = lines2
lines2 = []

for line in lines:
    flg = False
    index = -1

    for i in range(len(lines2)):
        line2 = lines2[i]
        for e in line:
            if e in line2:
                flg = True
                # line_target = line2
                index = i

                break

    if flg:
        for e in line:
            lines2[index].add(e)

    else:
        lines2.append(line)

####

checks = []
for line in lines2:
    for e in line:
        if e in checks:
            print("dup", e)
        else:
            checks.append(e)

map = {}

for line in lines2:
    key = None
    arr = []
    for e in line:
        if not key:
            key = e
        else:
            arr.append(e)

    map[key] = arr

######

dd = {}

for line in lines2:
    line = list(line)# list(copy.deepcopy(line))
    print(line)
    for e in line:
        line_c = copy.deepcopy(line)
        line_c.remove(e)
        dd[e] = line_c
        print(e, line, line_c, dd[e])

# dd = copy.deepcopy(map) #変更行

dd2 = {}

for key in map:
    for v in map[key]:
        # dd[v] = [key]
        dd2[v] = key

with open("data/itaiji_tobun.json", 'w') as outfile:
    json.dump(map, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

with open("data/dict_tobun.json", 'w') as outfile:
    json.dump(dd, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

with open("data/norm_tobun.json", 'w') as outfile:
    json.dump(dd2, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))