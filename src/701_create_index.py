
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

import datetime
now = datetime.datetime.now()
updated = "{0:%Y-%m-%d}".format(now)

prefix = "https://static.toyobunko-lab.jp/suikeichuzu"
prefix_data = "https://static.toyobunko-lab.jp/suikeichuzu_data"
docs = "../docs"

files = glob.glob('data/curation/*/curation.json')

actions = []

for file in files:

    print(file)

    with open(file) as f:
        curation = json.load(f)    

    manifest = curation["selections"][0]["within"]["@id"]

    members = curation["selections"][0]["members"]
    for i in range(len(members)):
        member = members[i]

        if i % 100 == 0:
            print(i+1, len(members))
    
        id = member["label"]

        id = id.replace("&nbsp;", "").replace("\n", "").strip()

        map = {}

        if "metadata" not in member:
            continue

        metadata = member["metadata"]

        for e in metadata:
            map[e["label"]] = e["value"]

        obj = {
            "objectID": id,
            "label": map["地名/記述"],
            # "_url" : app_prefix + "/item/"+id,
            "member": member["@id"],
            "manifest" : manifest,
            "curation" : prefix_data + "/curation/" + id  +".json"
        }

        fulltext = obj["label"]

        # if "thumbnail" in member:
        obj["thumbnail"] = member["thumbnail"]

        for key in map:
            obj[key] = [map[key]]
            try:
                fulltext += ", " + ", ".join(obj[key])
            except Exception as e:
                pass

        obj["fulltext"] = fulltext

        obj["_updated"] = updated

        # item = copy.deepcopy(obj)
        # item["_updated"] = "{0:%Y-%m-%d}".format(now)

        with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/item/{}.json".format(id), 'w') as outfile:
            json.dump(obj, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

        del obj["_updated"]
        actions.append(obj)

        # print(len(actions))


with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/index.json", 'w') as outfile:
    json.dump(actions, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))