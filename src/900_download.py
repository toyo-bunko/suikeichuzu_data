
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

df = requests.get("https://app.toyobunko-lab.jp/iiif/2/collection/suikeichuzu").json()

manifests = df["manifests"]

for m in manifests:
    uri = m["@id"]
    id = uri.split("/")[-2]

    df2 = requests.get(uri).json()

    path = "manifests/{}/manifest.json".format(id)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        json.dump(df2, f, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))