
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
    "https://nakamura196.github.io/suikeichuuzu/iiif/Saiiki/manifest.json": "https://app.toyobunko-lab.jp/iiif/2/f75e3194-194f-443c-bfa4-6eb50568c5ef"
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

    break



'''

map = {
    "main" : "https://api.jsonbin.io/b/60e2de56fe016b59dd5c8f8e/1",
    "etsunan" : "https://api.jsonbin.io/b/60e2e057fe016b59dd5c90de/1",
    "saiiki" : "https://api.jsonbin.io/b/60e2e0b055b7245a20d60b5b/1"
}

for id in map:
    url = map[id]

    df = requests.get(url).json()

    path = "data/tmp/" + id + "/manifest.json"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as outfile:
        json.dump(df, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

    canvase



ids = ["main", "etsunan", "saiiki"]

def handleManifests():

    files = glob.glob("../docs/iiif/sjzt_*/manifest.json")

    images_map = {}

    for file in files:

        with open(file) as f:
            m_data = json.load(f)

        canvases = m_data["sequences"][0]["canvases"]

        for canvas in canvases:
            id = canvas["@id"]
            filename = canvas["images"][0]["resource"]["@id"].split("/")[-1]
            images_map[filename] = {
                "canvas" : id,
                "manifest" : file.replace("../docs", "https://static.toyobunko-lab.jp/suikeichuzu_data")
            }

    # print(images_map.keys())

    return images_map

def handleMap():

    excel_path = "/Users/nakamurasatoru/git/d_toyo/app-suikeichuuzu/src/data/水経注図冊子画像-区画対応.xlsx"

    df = pd.read_excel(excel_path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

    r_count = len(df.index)
    c_count = len(df.columns)

    docs = {}
    labels = {}

    for j in range(1, r_count):
        c0 = df.iloc[j, 0]
        c1 = df.iloc[j, 1]
        c2 = df.iloc[j, 2].replace("冊", "")
        # print(id)
       
        # docs[c0+"-"+c1+"-"+c2] = df.iloc[j, 3]
        docs[c0 + c1] = df.iloc[j, 3]

        koma = int(df.iloc[j, 3].split("_")[1].split(".")[0])

        labels[c0 + c1] = c0 + c1 + ": " + df.iloc[j, 2] + " (" + str(koma) + "コマ目)"

    return docs, labels

docs, labels = handleMap()
images = handleManifests()

print(docs)

for id in ids:
    path = "/Users/nakamurasatoru/git/d_toyo/old_suikeichuzu/src/2021/data/curation/" + id + "/raw.json"

    print(id)

    with open(path) as f:
        curation = json.load(f)

    members = curation["selections"][0]["members"]

    members2 = []

    for i in range(len(members)):

        
        

        member = members[i]


        label = member["label"]

        
        if "(" not in label:
            # pass
            # print(label)

            if label not in docs:
                continue

            image = docs[label]

            info = images[image]



            url = "http://www.toyo-bunko.or.jp/research/ss/iiif/mirador/?manifest=" + info["manifest"] + "&canvas=" + info["canvas"]
            name = labels[label]

            metadata = []
            metadata.append({
                "label": "Annotation",
                "value": [
                    {
                        "@id": member["@id"] + "_anno",
                        "@type": "oa:Annotation",
                        "motivation": "sc:painting",
                        "on": member["@id"],
                        "resource": {
                            "@type": "cnt:ContentAsText",
                            "chars": "[ <a href=\"{}\">{}</a> ]".format(url, name),
                            "format": "text/html",
                            "marker": {
                                "@id": "https://static.toyobunko-lab.jp/suikeichuzu_data/assets/marker/0.png#xy=11,27",
                                "@type": "dctypes:Image"
                            }
                        }
                    }
                ]
            })

            member["metadata"] = metadata

            members2.append(member)

    curation["selections"][0]["members"] = members2

    with open("/Users/nakamurasatoru/git/d_toyo/suikeichuzu_data/docs/curation_book/" + id + ".json", 'w') as outfile:
        json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

        

'''