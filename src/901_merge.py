
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

with open("data/configs.json") as f:
    configs = json.load(f)


for conf in configs:
    m = None

    targets = conf["targets"]

    for target in targets:

        with open("manifests/{}/manifest.json".format(target)) as f:
            df = json.load(f)
            
            if m == None:
                m = df

                if len(targets) > 1:

                    resource = m["sequences"][0]["canvases"][0]["images"][0]["resource"]
                    
                    import copy
                    resource_org = copy.deepcopy(resource)

                    resource["@type"] = "oa:Choice"

                    resource["default"] = resource_org

                    resource["item"] = []

            else:
                m["sequences"][0]["canvases"][0]["images"][0]["resource"]["item"].append(df["sequences"][0]["canvases"][0]["images"][0]["resource"])


    path = "manifests/{}/manifest.json".format(conf["label"])

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        json.dump(m, f, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))