
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

rr = requests.get("https://wwwap.hi.u-tokyo.ac.jp/ships/itaiji_list.jsp")
html = rr.content
soup = BeautifulSoup(html, "html.parser")

print(str(soup))

trs = soup.find_all("tr")

map = {}

dd = {}

for tr in trs:
    tds = tr.find_all("td")

    if len(tds) != 3:
        continue

    # print(tds)

    key = tds[1].text.strip()
    vars = tds[2].text.replace("　", " ").split(" ")

    arr = []
    for v in vars:
        v = v.strip()
        if v != "":
            arr.append(v)

    map[key] = arr

dd = copy.deepcopy(map) #変更行

dd2 = {}

for key in map:
    for v in map[key]:
        dd[v] = [key]
        dd2[v] = key

with open("data/itaiji.json", 'w') as outfile:
    json.dump(map, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

with open("data/dict.json", 'w') as outfile:
    json.dump(dd, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

with open("data/norm.json", 'w') as outfile:
    json.dump(dd2, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))