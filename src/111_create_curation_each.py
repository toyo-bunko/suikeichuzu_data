
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
import shutil

with open('data/metadata.json') as f:
    metadata = json.load(f)

with open("data/legend.json") as f:
    legends = json.load(f)

settings = {
    "saiiki" : {
        "hash" : "600226dc9723af51efb6d9c366b062c3",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/1_003_Saiiki_gousei_l.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/Saiiki/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/saiiki/manifest.json"
           },
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/Saiiki/grid.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/saiiki/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/saiiki/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/f75e3194-194f-443c-bfa4-6eb50568c5ef/canvas/p1"
           },{
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/1_003_Saiiki_grid_l.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/1_003_Saiiki_gousei_l.tif"
           }
        ]
    },
    "etsunan" : {
        "hash" : "27fd1a30265116fbe0e6422974209f99",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/8_004_Etsunan_grid_l.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/Etsunan/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/etsunan/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/etsunan/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/c47580cf-b088-4e44-81fb-116060544348/canvas/p1"
           },{
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/Etsunan.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/8_004_Etsunan_grid_l.tif"
           }
        ]
    },
    "ukou" : {
        "hash" : "6b5ec55ca57758b4c39e1bb90c86d479",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/Ukou.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/Ukou/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/ukou/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/ukou/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/49946ae5-c6f8-4bbe-92d5-5a70c211b9ca/canvas/p1"
           },{
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/Ukou.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/Ukou.tif"
           }
        ]
    },
    "jouzu01_rekijou" : {
        "hash" : "99a80fdcdc846a12056b9880bdcfc6af",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu01_rekijou.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu01_rekijou/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu01_rekijou/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu01_rekijou/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu01_rekijou/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu01_rekijou.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu01_rekijou.tif"
           }
        ]
    },
    "jouzu02_gyoujou" : {
        "hash" : "86fc8366885e58ec808b95d38c01ddb2",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu02_gyoujou.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu02_gyoujou/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu02_gyoujou/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu02_gyoujou/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu02_gyoujou/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu02_gyoujou.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu02_gyoujou.tif"
           }
        ]
    },
    "jouzu03_rakuyou" : {
        "hash" : "1bd29b910178d0b6379c143a62c9a629",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu03_rakuyou.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu03_rakuyou/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu03_rakuyou/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu03_rakuyou/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu03_rakuyou/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu03_rakuyou.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu03_rakuyou.tif"
           }
        ]
    },
    "jouzu04_chouan" : {
        "hash" : "c4a34b738d30fe90fe83e78b2bbc9966",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu04_chouan.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu04_chouan/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu04_chouan/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu04_chouan/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu04_chouan/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu04_chouan.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu04_chouan.tif"
           }
        ]
    },
    "jouzu05_suiyou" : {
        "hash" : "97e9257593c4567a69cf86920b455fc8",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu05_suiyou.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu05_suiyou/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu05_suiyou/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu05_suiyou/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu05_suiyou/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu05_suiyou.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu05_suiyou.tif"
           }
        ]
    },
    "jouzu06_heijou" : {
        "hash" : "20be61f217fffbc94c12395db4120ec7",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu06_heijou.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu06_heijou/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu06_heijou/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu06_heijou/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu06_heijou/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu06_heijou.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu06_heijou.tif"
           }
        ]
    },
    "jouzu07_keijou" : {
        "hash" : "c9406bab532db460ff8c119d69ad5984",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu07_keijou.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu07_keijou/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu07_keijou/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu07_keijou/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu07_keijou/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu07_keijou.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu07_keijou.tif"
           }
        ]
    },
    "jouzu08_rojou" : {
        "hash" : "65a910994c0d4bc5bec2464c2c5871e3",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu08_rojou.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu08_rojou/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu08_rojou/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu08_rojou/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu08_rojou/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu08_rojou.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu08_rojou.tif"
           }
        ]
    },
    "jouzu09_rinshi" : {
        "hash" : "d1f5a800de359d7d605935a0f0219ea5",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu09_rinshi.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu09_rinshi/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu09_rinshi/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu09_rinshi/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu09_rinshi/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu09_rinshi.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu09_rinshi.tif"
           }
        ]
    },
    "jouzu10_jouyou" : {
        "hash" : "b4ee5c48a77b85fa2d9f9d03e7d050fa",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu10_jouyou.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu10_jouyou/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu10_jouyou/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu10_jouyou/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu10_jouyou/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu10_jouyou.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu10_jouyou.tif"
           }
        ]
    },
    "jouzu11_jushun" : {
        "hash" : "1056d3b2ef8a61fda18cc3b368e4dad2",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu11_jushun.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu11_jushun/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu11_jushun/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu11_jushun/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu11_jushun/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu11_jushun.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu11_jushun.tif"
           }
        ]
    },
    "jouzu12_seito" : {
        "hash" : "3f6b7a39e8eed39e3925c26362aa7147",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu12_seito.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu12_seito/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu12_seito/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu12_seito/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu12_seito/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu12_seito.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu12_seito.tif"
           }
        ]
    },
    "jouzu13_sanin" : {
        "hash" : "a47cddf2979d5c7fd527d8336a98affc",
        "image" : "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu13_sanin.tif",
        "reps" : [
           {
               "b": "https://nakamura196.github.io/suikeichuuzu/iiif/jouzu13_sanin/manifest.json",
               "a": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu13_sanin/manifest.json"
           },
           {
               "b": "https://static.toyobunko-lab.jp/suikeichuzu_data/iiif/jouzu13_sanin/manifest.json/canvas/p1",
               "a": "https://app.toyobunko-lab.jp/iiif/2/jouzu13_sanin/canvas/p1"
           },
           {
               "b": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/jouzu13_sanin.tif",
               "a": "https://img.toyobunko-lab.jp/iiif/premodern_chinese/suikeichuzu/jouzu13_sanin.tif"
           }
        ]
    }
}

prefix = "https://static.toyobunko-lab.jp/suikeichuzu"
prefix_data = "https://static.toyobunko-lab.jp/suikeichuzu_data"
docs = "../docs"

for uuid in settings:
    # uuid = "jouzu13_sanin"

    setting = settings[uuid]

    # image = setting["image"]

    

    with open('data/metadata.json') as f:
        metadata = json.load(f)

    dir = "/Users/nakamurasatoru/git/d_omeka/omekac_diyhistory"

    ##############

    rows = []

    key = uuid

    hash = setting["hash"]

    curation_ids = []

    print("***", key)

    file = dir + "/docs/iiif/curation/"+hash+"/curation.json"

    with open(file) as f:
        curation = json.load(f)

        curation_str = json.dumps(curation)

        if "reps" in setting:
            for rep in setting["reps"]:

                curation_str = curation_str.replace(rep["b"], rep["a"])
            
            curation = json.loads(curation_str)

    manifest = curation["selections"][0]["within"]["@id"]

    m = requests.get(manifest).json()

    image = m["sequences"][0]["canvases"][0]["images"][0]["resource"]["service"]["@id"]

    members = curation["selections"][0]["members"]

    members_map = {}

    for member in members:
        label = member["label"]

        label = label.split("&nbsp;")[0].strip()

        label = label.replace("&nbsp;", "").replace("\n", "").strip()

        if label in curation_ids:
            print("dupppp", label)
            continue
        else:
            curation_ids.append(label)

        if label not in metadata:
            print("not in metadata", label)
            continue

        metadata_new = []

        obj = metadata[label]

        for key2 in obj:
            value = obj[key2]
            
            if value == "null":
                continue

            metadata_new.append({
                "label" : key2,
                "value" : obj[key2]
            })

        member["metadata"] = metadata_new

        xywh = member["@id"].split("=")[1]

        member["thumbnail"] = image + "/"+xywh+"/200,/0/default.jpg"

        members_map[obj["sort"]] = member

    members = []
    for sort in sorted(members_map):
        # print("sort", sort)
        members.append(members_map[sort])
    curation["selections"][0]["members"] = members


    ofile = "data/curation/"+uuid+"/curation.json"

    dirname = os.path.dirname(ofile)
    os.makedirs(dirname, exist_ok=True)

    f2 = open(ofile, 'w')
    json.dump(curation, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

    # オリジナル
    shutil.copyfile(file, ofile.replace("curation.json", "raw.json"))

    # テスト
    curation_test = copy.deepcopy(curation)

    members = curation_test["selections"][0]["members"]

    for i in range(len(members)):
        member = members[i]

        id = member["label"]

        map = {}

        if "metadata" not in member:
            print("no metadata", id)
            continue

        for e in member["metadata"]:
            map[e["label"]] = e["value"]
        
        # del member["metadata"]

        mark = str(map["記号"])
        legend = legends[mark]

        '''
        {
            "value": "[ <a href=\"{}\">{}</a> ]<br/>地名/記述：{}<br/>分類：{}{}".format(prefix+"/item/"+ id, id, map["地名/記述"], legend["分類"], "<br/>記号説明：" + legend["記号説明"] if legend["記号説明"] != "" else ""),
            "label": "Description"
        }
        '''

        member["metadata"].append({
            "value": [
            {
                "@id": member["@id"]+"_anno",
                "on": member["@id"],
                "@type": "oa:Annotation",
                "resource": {
                "chars": "[ <a href=\"{}\">{}</a> ]<br/>地名/記述：{}<br/>分類：{}{}".format(prefix+"/item/"+ id, id, map["地名/記述"], legend["分類"], "<br/>記号説明：" + legend["記号説明"] if legend["記号説明"] != "" else ""),
                "format": "text/html",
                "@type": "cnt:ContentAsText",
                "marker": {
                    "@type": "dctypes:Image",
                    "@id": prefix_data + "/assets/marker/{}.png#xy=11,27".format(mark), # "https://nakamura196.github.io/suikeichuuzu/asset/marker/{}.png#xy=11,27".format(mark)
                }
                },
                "motivation": "sc:painting"
            }
            ],
            "label": "Annotation"
        })


        
        '''
        member["metadata"] = [

            {
              "value": [
                {
                  "@id": member["@id"]+"_anno",
                  "on": member["@id"],
                  "@type": "oa:Annotation",
                  "resource": {
                    "chars": "[ <a href=\"{}\">{}</a> ]<br/>地名/記述：{}<br/>分類：{}{}".format(prefix+"/item/"+ id, id, map["地名/記述"], legend["分類"], "<br/>記号説明：" + legend["記号説明"] if legend["記号説明"] != "" else ""),
                    "format": "text/html",
                    "@type": "cnt:ContentAsText",
                    "marker": {
                      "@type": "dctypes:Image",
                      "@id": prefix_data + "/assets/marker/{}.png#xy=11,27".format(mark), # "https://nakamura196.github.io/suikeichuuzu/asset/marker/{}.png#xy=11,27".format(mark)
                    }
                  },
                  "motivation": "sc:painting"
                }
              ],
              "label": "Annotation"
            }
          ]
        '''

        ########

        rows.append({
            "id" : id,
            "label" : map["地名/記述"],
            "category" : map["記号"],
            "manifest" : prefix_data + "/iiif/"+uuid+"/manifest.json",
            "member" : member["@id"]
        })

    curation_test["viewingHint"] = "annotation"
    curation_test["related"] = {
        "@type": "cr:MarkerLegend",
        "@id": prefix_data + "/assets/legend.pdf",
    }
    curation_test["label"] = uuid

    curation_test["@id"] = prefix_data + "/curation/"+uuid+".json"

    path = curation_test["@id"].replace(prefix_data, docs)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    f2 = open(path, 'w')
    json.dump(curation_test, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

    f2 = open("data/rows.json", 'w')
    json.dump(rows, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

