
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

def getIndex():
    map = {}
    with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/index_river.json") as f:
        dd = json.load(f)

    for obj in dd:
        map[obj["objectID"]] = obj    

    return map

files = glob.glob("/Users/nakamurasatoru/git/d_toyo/suikeichuzu_data/docs/curation_01/*.json")

map = getIndex()

for file in files:
    with open(file) as f:
        m_data = json.load(f)

        members = m_data["selections"][0]["members"]

        for member in members:
            metadata = member["metadata"]

            id = member["label"]

            id = id.replace("&nbsp;", "").strip()

            data = map[id]

            keys = ["水名", "水経注：巻"]

            for key in keys:
                if key in data:
                    metadata.append({
                        "label": key,
                        "value" : data[key]
                    })

    with open(file.replace("curation_01", "curation"), 'w') as outfile:
        json.dump(m_data, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
        

'''
def handleManifests():

    files = glob.glob("../docs/iiif/sjzt_*/manifest.json")

    images_map = {}

    for file in files:

        with open(file) as f:
            m_data = json.load(f)

        canvases = m_data["sequences"][0]["canvases"]

        for canvas in canvases:
            id = canvas["@id"]
            filename = canvas["images"][0]["resource"]["@id"].split("/")[-1]
            images_map[filename] = {
                "canvas" : id,
                "manifest" : file.replace("../docs", "https://static.toyobunko-lab.jp/suikeichuzu_data")
            }

    # print(images_map.keys())

    return images_map

def handleMap():

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

    return docs

# print(docs)

with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/index_river.json") as f:
    dd = json.load(f)

docs = handleMap()
images = handleManifests()

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

    id = item["objectID"]

    # print(item["objectID"])
    if slug in docs:
        # print()
        filename = docs[slug]
        info = images[filename]

        item["水経注図：冊子画像"] = ["http://www.toyo-bunko.or.jp/research/ss/iiif/mirador/?manifest=" + info["manifest"] + "&canvas=" + info["canvas"]]



    with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/item/"+id+".json", 'w') as outfile:
        json.dump(item, outfile, ensure_ascii=False,
                    indent=4, sort_keys=True, separators=(',', ': '))

    if "水経注図：冊子画像" in item:
        del item["水経注図：冊子画像"]


with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/index_book.json", 'w') as outfile:
    json.dump(dd, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

'''