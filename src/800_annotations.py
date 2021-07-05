
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

ids = ["saiiki", "main", "etsunan"]

reps = {
    "https://nakamura196.github.io/suikeichuuzu/iiif/Saiiki/manifest.json": "https://app.toyobunko-lab.jp/iiif/2/f75e3194-194f-443c-bfa4-6eb50568c5ef",
    "https://nakamura196.github.io/suikeichuuzu/iiif/main": "https://app.toyobunko-lab.jp/iiif/2/f772d9f6-2893-4b2c-8cd2-600f87b8583e",
    "https://nakamura196.github.io/suikeichuuzu/iiif/Etsunan/manifest.json" : "https://app.toyobunko-lab.jp/iiif/2/c47580cf-b088-4e44-81fb-116060544348"
}

for id in ids:
    path = "../docs/iiif/" + id + "/manifest.json"
    with open(path) as f:
        m_data = json.load(f)

    print(m_data)

    path = "../docs/curation_book/" + id + ".json"
    with open(path) as f:
        curation = json.load(f)

    print(curation)

    

    resources = []

    members = curation["selections"][0]["members"]

    for i in range(len(members)):
        member = members[i]

        mid = member["@id"]

        for r in reps:
            mid = mid.replace(r, reps[r])

        resources.append({
            "@id": mid+"_annolist",
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "resource": [
                {
                "@type": "dctypes:Text",
                "chars": member["metadata"][0]["value"][0]["resource"]["chars"],
                "format": "text/html"
                }
            ],
            "on": mid
        })

    annolist = {

        "@id": m_data["@id"].replace("manifest.json", "annolist.json"),
        "@context": "http://www.shared-canvas.org/ns/context.json",
        "@type": "sc:AnnotationList",
        "resources": resources,
        
    }

    opath = "../docs/iiif/" + id + "/annolist.json"

    os.makedirs(os.path.dirname(opath), exist_ok=True)

    with open(opath, 'w') as outfile:
        json.dump(annolist, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

    #######

    m_data["sequences"][0]["canvases"][0]["otherContent"] = [
        {
            "@id": annolist["@id"],
            "@type": "sc:AnnotationList"
        }
    ]

    with open("../docs/iiif/" + id + "/manifest_anno.json", 'w') as outfile:
        json.dump(m_data, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))