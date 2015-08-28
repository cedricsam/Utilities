#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import stat
import csv
import json
import types
import argparse

attrs = ["geometryType", "spatialReference"]
geometryType = spatialReference = None
cols = []

ap = argparse.ArgumentParser(description='Parse JSON file from an ArcGIS REST API file')
ap.add_argument('infile', nargs='?', type=argparse.FileType('r'), const=sys.stdin, default=sys.stdin)
ap.add_argument('outfile', nargs='?', type=argparse.FileType('a'), const=sys.stdout, default=sys.stdout)
ap.add_argument('--headers', dest='headers', action='store_true')
ap.add_argument('--no-headers', dest='headers', action='store_false')
ap.set_defaults(headers=False)

args = ap.parse_args()

try:
    js = json.loads(args.infile.read())
except:
    print >> sys.stderr, args.infile
    sys.exit()

if "spatialReference" in js and "wkid" in js["spatialReference"]:
    spatialReference = js["spatialReference"]["wkid"]

if "geometryType" in js:
    geometryType = js["geometryType"]

fields = []
for field in js["fields"]:
    fields.append(field["name"])

outrows = []
for feature in js["features"]:
    r = {}
    r["spatialreference"] = spatialReference
    r["geometrytype"] = geometryType
    for a in fields:
        r[a.lower()] = feature["attributes"][a]
    geomtype = "POLYGON"
    if "geometry" in feature:
        r["geometry"] = re.sub(r" +", " ", re.sub(r"\], ?\[","|", re.sub(r"\]\], ?\[\[", ")|(", re.sub(r"\]\]\]$", "))", re.sub(r"^\[\[\[","SRID="+spatialReference+";"+geomtype+"((",str(feature["geometry"]["rings"]))))).replace("[","").replace("]","").replace(","," ").replace("|",","))
    #r.time_fetched = time_fetched
    outrows.append(r)

cols = []
for c in attrs:
    cols.append(c.lower())
for c in fields:
    cols.append(c.lower())
cols.append("geometry")

cw = csv.DictWriter(args.outfile, cols)

if args.headers:
    cw.writeheader()
cw.writerows(outrows)
