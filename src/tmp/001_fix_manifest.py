
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

files = glob.glob("../../docs/iiif/sjzt_*/manifest.json")

for file in files:
    print(file)

    with open(file) as f:
        df = json.load(f)

        df["attribution"] = "東洋文庫 / Toyo Bunko"
        df["license"] = "二次利用不可"

        canvases = df["sequences"][0]["canvases"]

        for canvas in canvases:
            resource = canvas["images"][0]["resource"]
            id = resource["@id"]
            resource["service"] = {
                "@context": "http://iiif.io/api/image/2/context.json",
                "@id": id,
                "profile": "http://iiif.io/api/image/2/level1.json"
            }
            resource["@id"] = id + "/full/full/0/default.jpg"

            canvas["thumbnail"] = {
                "@id": id + "/full/!200,200/0/default.jpg",
                "@type": "dctypes:Image",
                "format": "image/jpeg",
            }



    with open(file, 'w') as f:
        json.dump(df, f, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))