
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
    id = obj["objectID"]

    if "城" in obj["図"][0]:
        key = obj["図"][0]
    else:

        区画南北 = str(obj["区画南北"][0])
        区画東西 = str(obj["区画東西"][0])

        key = 区画南北 + 区画東西

    if "西域" in obj["図"][0]:
        key = "西域" + key

    # 旧字対応 

    key = key.replace("図", "圖")

    if key not in river:
        river[key] = []

    river[key].append(id)

with open("data/river.json", 'w') as outfile:
    json.dump(river, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))