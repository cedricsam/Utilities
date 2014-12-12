#!/usr/bin/env python

import sys
import os
import json
import csv

fslides = open(sys.argv[1],"r")
fplaces = open(sys.argv[2],"r")

numcols = []

slides = csv.DictReader(fslides)
places = csv.DictReader(fplaces)

ss = []
for slide in slides:
    mks = []
    for place in places:
        for a in numcols:
            if a in place and place[a] is not None and len(place[a]) > 0:
                try:
                    place[a] = float(place[a])
                except:
                    pass
        slideids = place["slide"].split(",")
        for slideid in slideids:
            if slideid == slide["id"]:
                mks.append(place)
                break
    slide["markers"] = mks
    ss.append(slide)
    fplaces.seek(0)
    for a in numcols:
        if a in slide and slide[a] is not None and len(slide[a]) > 0:
            try:
                slide[a] = float(slide[a])
            except:
                pass
    places = csv.DictReader(fplaces)

t = """window.markerTypes = {
  "family": "marker-fam",
  "gov":    "marker-gov",
  "video":   "marker-video",
  "picture":   "marker-picture",
  "news":   "marker-news",
  "social": "marker-soc"
};
window.infoTypes = {
  "picture": "info-picture",
  "video":   "info-video",
  "youtube":   "info-youtube",
  "tweet":   "info-tweet"
};
"""

print t

print "window.mapInfo = " + json.dumps(ss, indent=4, separators=(',', ': ')) + ";"
