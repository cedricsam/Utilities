#!/usr/bin/env python

import sys
import simplejson

sep = ","

if len(sys.argv) <= 1:
    print "Missing file"
    sys.exit()

cp = sys.argv[1].split("/")[len(sys.argv[1].split("/"))-1].split(".")[0]
f = open(sys.argv[1], "r")
js = simplejson.loads(f.read())
#print js
if "results" not in js or len(js["results"]) <= 0:
    sys.exit()
res = js["results"][0]
geom = res["geometry"]
loc = geom["location"]
lat = loc["lat"]
lng = loc["lng"]

print cp + sep + str(lat) + sep + str(lng)
