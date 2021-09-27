
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

ids = ["main", "saiiki", "etsunan", "ukou", 

"jouzu01_rekijou", 
"jouzu02_gyoujou", 
"jouzu03_rakuyou", 
"jouzu04_chouan", 
"jouzu05_suiyou", 
"jouzu06_heijou", 
"jouzu07_keijou", 
"jouzu08_rojou", 
"jouzu09_rinshi", 
"jouzu10_jouyou", 
"jouzu11_jushun", 
"jouzu12_seito", 
"jouzu13_sanin", 
]

manifests = []

prefix = "https://static.toyobunko-lab.jp/suikeichuzu_data"
dir = "../docs"

for id in ids:

    print(id)

    with open("manifests/{}/manifest.json".format(id)) as f:
        df = json.load(f)

        

        df["@id"] = prefix + "/iiif/" + id + "/manifest.json"

        path = df["@id"].replace(prefix, dir)

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w') as f:
            json.dump(df, f, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
        
        # manifests.append(df)

        df2 = {
            "@id" : df["@id"],
            "label" : df["label"],
            "@type" : "sc:Manifest",
            "thumbnail" : df["thumbnail"]["@id"]
        }
        manifests.append(df2)

collection = {
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": prefix + "/iiif/collection/top.json",
  "@type": "sc:Collection",
  "label": "水経注図",
  "attribution": "東洋文庫 / Toyo Bunko",
  "vhint": "use-thumb",
  "manifests": manifests
}

path = collection["@id"].replace(prefix, dir)

os.makedirs(os.path.dirname(path), exist_ok=True)

with open(path, 'w') as f:
    json.dump(collection, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))