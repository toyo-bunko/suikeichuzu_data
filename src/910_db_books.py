
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

with open("../docs/iiif/collection/sjzt.json") as f:
    df = json.load(f)

collections = []

manifests = []
collection = {
    "label" : "冊子画像一覧",
    "@id": df["@id"],
    "@type" : "sc:Collection",
    "manifests" : manifests
}
collections.append(collection)


for m in df["manifests"]:
    path = m["@id"].replace("https://static.toyobunko-lab.jp/suikeichuzu_data", "../docs")

    with open(path) as f:
        df2 = json.load(f)

    # マニフェストの修正
    df2["@id"] = m["@id"]

    if "related" in df2:
        del df2["related"]

    thumbnail = df2["sequences"][0]["canvases"][0]["thumbnail"]["@id"]

    df2["thumbnail"]["@id"] = thumbnail
    df2["label"] = "水経注図・" + m["label"]

    manifests.append({
        "@id": m["@id"],
        "@type": "sc:Manifest",
        "label" : m["label"],
        "thumbnail" : thumbnail
    })

    with open(path, 'w') as f:
        json.dump(df2, f, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))

ids = ["main", "saiiki", "etsunan"]

manifests2 = []
collection2 = {
    "label" : "画像からみる",
    "@type" : "sc:Collection",
    "manifests" : manifests2,
    "description" : "ビューア左部の「Layers」タブを利用することにより、グリッド画像を重ねて表示できます。"
}
collections.append(collection2)

for id in ids:
    path = "../docs/iiif/" + id + "/manifest_anno.json"
    with open(path) as f:
        df = json.load(f)

    manifests2.append({
        "@id": df["@id"].replace("manifest.json", "manifest_anno.json"),
        "@type": "sc:Manifest",
        "label" : df["label"],
        "thumbnail" : df["thumbnail"]["@id"]
    })

collection = {
    "label" : "冊子画像",
    "@type" : "sc:Collection",
    "@id" : "https://static.toyobunko-lab.jp/suikeichuzu_data" + "/iiif/collection/books.json",
    "collections": collections,
    "vhint" : "use-thumb"
}

with open("../docs/iiif/collection/books.json", 'w') as outfile:
    json.dump(collection, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))