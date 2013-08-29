#!/usr/bin/env python

import sys
import json
import csv
import types

if len(sys.argv) <= 1:
    print "Missing file"
    sys.exit()

cols = ["id","lat","lng","location_type","bbox_n","bbox_e","bbox_s","bbox_w","viewport_n","viewport_e","viewport_s","viewport_w","formatted_address"]
id = sys.argv[1].split("/")[len(sys.argv[1].split("/"))-1].split(".")[0]
f = open(sys.argv[1], "r")
js = json.loads(f.read())
#print js
if "results" not in js or len(js["results"]) <= 0:
    sys.exit()
res = js["results"][0]
geom = res["geometry"]
loc = geom["location"]
r = dict()
r["id"] = id
r["lat"] = loc["lat"]
r["lng"] = loc["lng"]
r["formatted_address"] = res["formatted_address"]
r["location_type"] = geom["location_type"]
bbox = geom["bounds"]
r["bbox_n"] = bbox["northeast"]["lat"]
r["bbox_e"] = bbox["northeast"]["lng"]
r["bbox_s"] = bbox["southwest"]["lat"]
r["bbox_w"] = bbox["southwest"]["lng"]
viewport = geom["viewport"]
r["viewport_n"] = viewport["northeast"]["lat"]
r["viewport_e"] = viewport["northeast"]["lng"]
r["viewport_s"] = viewport["southwest"]["lat"]
r["viewport_w"] = viewport["southwest"]["lng"]

for a in cols:
    if type(r[a]) is types.StringType or type(r[a]) is types.UnicodeType:
        try:
            r[a] = r[a].encode("utf8")
        except:
            continue

cw = csv.DictWriter(sys.stdout, cols)
cw.writerow(r)
