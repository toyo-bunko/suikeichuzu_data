
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

excel_path = "/Users/nakamurasatoru/git/d_toyo/app-suikeichuuzu/src/data/水経注図冊子画像-区画対応.xlsx"

df = pd.read_excel(excel_path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

r_count = len(df.index)
c_count = len(df.columns)

docs = {}

for j in range(1, r_count):
    c0 = df.iloc[j, 0]
    c1 = df.iloc[j, 1]
    c2 = df.iloc[j, 2].replace("冊", "")
    # print(id)
    docs[c0+"-"+c1+"-"+c2] = df.iloc[j, 3]

print(docs)

with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/index_river.json") as f:
    dd = json.load(f)

map = {}

for item in dd:
    表裏 = item["表裏"][0]
    図 = item["図"][0]
    冊 = item["冊"][0]

    区画南北 = item["区画南北"][0]
    区画東西 = item["区画東西"][0]

    if "城" in 図:
        slug = "{}-{}-{}".format(図, 表裏, 冊)
    else:
        slug = "{}{}-{}-{}".format(区画南北, 区画東西, 表裏, 冊)

    '''
    if slug not in map:
        map[slug] = []
    map[slug].append(item["objectID"])
    '''
    print(item["objectID"])
    if slug in docs:
        print(docs[slug])

# for docs

'''

with open("/Users/nakamurasatoru/git/d_toyo/app-suikeichuuzu/static/data/curation.json") as f:
    dd = json.load(f)

selections = dd["selections"]

for selection in selections:
    print(selection["within"])

'''

'''
with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/index.json", 'w') as outfile:
    json.dump(actions, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
'''