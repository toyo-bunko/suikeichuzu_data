
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

import yaml

with open('../config.yml') as file:
    config = yaml.safe_load(file)

mirador = config["data_url"] + "/mirador"

def handleManifests():

    files = glob.glob("../docs/iiif/sjzt_*/manifest.json")

    images_map = {}

    for file in files:

        with open(file) as f:
            m_data = json.load(f)

        canvases = m_data["sequences"][0]["canvases"]

        for canvas in canvases:
            id = canvas["@id"]
            filename = canvas["images"][0]["resource"]["@id"].split("/")[-5].replace(".tif", ".jpg")
            images_map[filename] = {
                "canvas" : id,
                "manifest" : file.replace("../docs", "https://static.toyobunko-lab.jp/suikeichuzu_data")
            }

    return images_map

def handleMap():

    excel_path = "../data/etc/水経注図冊子画像-区画対応.xlsx"

    df = pd.read_excel(excel_path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

    r_count = len(df.index)

    docs = {}

    for j in range(1, r_count):
        c0 = df.iloc[j, 0]
        c1 = df.iloc[j, 1]
        c2 = df.iloc[j, 2].replace("冊", "")
        # print(id)
        docs[c0+"-"+c1+"-"+c2] = df.iloc[j, 3]

    return docs

with open(config["app_dir"] + "/static/data/index_river.json") as f:
    dd = json.load(f)

docs = handleMap()
images = handleManifests()

for i in range(len(dd)):
    item = dd[i]

    if i % 100 == 0:
        print(i+1, len(dd), item["objectID"])

    表裏 = item["表裏"][0]
    図 = item["図"][0]
    冊 = item["冊"][0]

    区画南北 = item["区画南北"][0]
    区画東西 = item["区画東西"][0]

    if "城" in 図:
        slug = "{}-{}-{}".format(図, 表裏, 冊)
    elif 図 in ["西域", "越南"]:
        slug = "{}{}{}-{}-{}".format(図, 区画南北, 区画東西, 表裏, 冊)
    else:
        slug = "{}{}-{}-{}".format(区画南北, 区画東西, 表裏, 冊)

    id = item["objectID"]

    if slug in docs:
        filename = docs[slug]
        info = images[filename]
        item["水経注図：冊子画像"] = [mirador + "?manifest=" + info["manifest"] + "&canvas=" + info["canvas"]]
    else:
        print("NONE", id, slug)

    with open(config["app_dir"] + "/static/data/item/"+id+".json", 'w') as outfile:
        json.dump(item, outfile, ensure_ascii=False,
                    indent=4, sort_keys=True, separators=(',', ': '))

    if "水経注図：冊子画像" in item:
        del item["水経注図：冊子画像"]


with open(config["app_dir"] + "/static/data/index_book.json", 'w') as outfile:
    json.dump(dd, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))