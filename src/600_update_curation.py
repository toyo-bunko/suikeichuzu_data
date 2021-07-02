
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

            墨朱 = ""

            for m in metadata:
                if m["label"] == "Annotation":
                    chars = m["value"][0]["resource"]["chars"]

                if m["label"] == "墨朱":
                    墨朱 = m["value"]

            for m in metadata:
                if m["label"] == "Annotation":
                    chars = m["value"][0]["resource"]["chars"]

                    '''
                    if m["label"] == "墨朱":
                        墨朱 = m["value"]
                    '''

                    if 墨朱 != "":
                         m["value"][0]["resource"]["chars"] = chars + "<br/>墨朱：" + 墨朱

            

    with open(file.replace("curation_01", "curation"), 'w') as outfile:
        json.dump(m_data, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))