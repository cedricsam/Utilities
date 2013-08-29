#!/usr/bin/env python

import sys
import json
import csv
import types
import os.path, time

cols = ["id","pos","geocodetime","lang","lat","lng","location_type","bbox_n","bbox_e","bbox_s","bbox_w","viewport_n","viewport_e","viewport_s","viewport_w","formatted_address","types"]#,"country","postal_code","administrative_area_level_1","administrative_area_level_2","locality","sublocality","route"]
components = ["country","postal_code","postal_code_prefix","administrative_area_level_1","administrative_area_level_2","administrative_area_level_3","locality","sublocality","neighborhood","route"]
for component in components:
    cols.append(component + "_long_name")
    cols.append(component + "_short_name")
cw = csv.DictWriter(sys.stdout, cols)

if len(sys.argv) <= 1:
    #print "Missing file"
    cw.writeheader()
    sys.exit()
else:
    id = sys.argv[1].split("/")[len(sys.argv[1].split("/"))-1].split(".")[0]
    f = open(sys.argv[1], "r")
    js = json.loads(f.read())
if len(sys.argv) > 2:
    lang = sys.argv[2]
else:
    lang = "fr"

try:
    t = time.gmtime(os.path.getmtime(sys.argv[1]))
    t = time.strftime("%Y-%m-%d %H:%M:%S", t)
except:
    t = None

if "results" not in js or len(js["results"]) <= 0:
    sys.exit()
for pos in range(len(js["results"])):
    res = js["results"][pos]
    geom = res["geometry"]
    loc = geom["location"]
    r = dict()
    r["id"] = id
    r["pos"] = pos
    r["lang"] = lang
    r["geocodetime"] = t
    r["lat"] = loc["lat"]
    r["lng"] = loc["lng"]
    r["formatted_address"] = res["formatted_address"]
    if "location_type" in geom:
        r["location_type"] = geom["location_type"]
    if "bounds" in geom:
        bbox = geom["bounds"]
        r["bbox_n"] = bbox["northeast"]["lat"]
        r["bbox_e"] = bbox["northeast"]["lng"]
        r["bbox_s"] = bbox["southwest"]["lat"]
        r["bbox_w"] = bbox["southwest"]["lng"]
    if "viewport" in geom:
        viewport = geom["viewport"]
        r["viewport_n"] = viewport["northeast"]["lat"]
        r["viewport_e"] = viewport["northeast"]["lng"]
        r["viewport_s"] = viewport["southwest"]["lat"]
        r["viewport_w"] = viewport["southwest"]["lng"]
    if "types" in res:
        r["types"] = "|".join(res["types"])    
    for ac in res["address_components"]:
        if ac["types"][0] in components:
            if "long_name" in ac: r[ac["types"][0] + "_long_name"] = ac["long_name"]
            if "short_name" in ac: r[ac["types"][0] + "_short_name"] = ac["short_name"]
    for a in cols:
        if a in r and (type(r[a]) is types.StringType or type(r[a]) is types.UnicodeType):
            try:
                r[a] = r[a].encode("utf8")
            except:
                continue
    cw.writerow(r)
