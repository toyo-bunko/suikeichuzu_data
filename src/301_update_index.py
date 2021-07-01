
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
    index = json.load(f)

with open("data/river.json") as f:
    river = json.load(f)

with open("/Users/nakamurasatoru/git/d_toyo/old_suikeichuzu/src/river/data/river.json") as f:
    river_org = json.load(f)

map = {}

for area in river:
    print(area)

    ids = river[area]

    if area not in river_org:
        print("missing area", area)
        continue

    config = river_org[area]

    for id in ids:
        map[id] = {
            "river": [],
            "vol": []
        }

        for key2 in config:
            river2 = config[key2]["value"]
            vol = config[key2]["vol"]

            if river2 not in map[id]["river"]:
                map[id]["river"].append(river2)

            if vol not in map[id]["vol"]:
                map[id]["vol"].append(vol)

for item in index:
    id = item["objectID"]

    if id not in map:
        print("id missing", id)
        continue

    config = map[id]

    item["水経注：巻"] = config["vol"]
    item["水名"] = config["river"]

with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu/static/data/index_river.json", 'w') as outfile:
    json.dump(index, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))