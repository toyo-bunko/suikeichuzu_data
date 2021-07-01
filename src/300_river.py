
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

with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/index.json") as f:
    df = json.load(f)

river = {}

for obj in df:
    print(obj)

    id = obj["objectID"]

    if "城" in obj["図"][0]:
        key = obj["図"][0]
    else:

        区画南北 = str(obj["区画南北"][0])
        区画東西 = str(obj["区画東西"][0])

        key = 区画南北 + 区画東西

    if "西域" in obj["図"][0]:
        key = "西域" + key

    if key not in river:
        river[key] = []

    river[key].append(id)

    # break

'''
def itaiji(data):
    for key in dd:
        for v in dd[key]:
            data = data.replace(v, key)

    return data

for file in files:

    print(file)

    dirname = file.split("/")[-2]

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
            "curation" : prefix_data + "/curation/" + dirname  +".json"
        }

        fulltext = obj["label"] + ", " + id

        # if "thumbnail" in member:
        obj["thumbnail"] = member["thumbnail"]

        for key in map:
            obj[key] = [map[key]]
            try:
                fulltext += ", " + ", ".join(obj[key])
            except Exception as e:
                pass

        fulltext = itaiji(fulltext)

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
'''

for key in river:
    print(key)

with open("data/river.json", 'w') as outfile:
    json.dump(river, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))