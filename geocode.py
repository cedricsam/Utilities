#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import argparse
import urllib
import json
import re
import os
import time

ap = argparse.ArgumentParser(description='Geocode data from a file')
ap.add_argument('idcols', nargs='?', default="1")
ap.add_argument('geocols', nargs='?', default="2-")
ap.add_argument('dir', nargs='?', default="geocode")
ap.add_argument('infile', nargs='?', type=argparse.FileType('r'), const=sys.stdin, default=sys.stdin)
args = ap.parse_args()

DIR = args.dir
GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"

geocoding_api_default_args = {"sensor":"false","language":"en","region":"hk","components":"country:HK"}

idcols_arr = args.idcols.split(",")
geocols_arr = args.geocols.split(",")

incols_arr = [idcols_arr, geocols_arr]
to_geocode_cols_arr = [list(), list()]

cr = csv.reader(args.infile)
inrows = list()
row_max_length = 0
for r in cr:
    inrows.append(r)
    row_max_length = max(row_max_length, len(r))
print row_max_length

for cols_arr_i in range(len(incols_arr)):
    cols_arr = incols_arr[cols_arr_i]
    cols_arr_list = []
    for cols in cols_arr:
        if "-" in cols:
            range_cols = cols.split("-")
            try:
                start_range = int(range_cols[0])-1
            except:
                start_range = 0
            try:
                end_range = int(range_cols[1])
            except:
                end_range = row_max_length
            for i in range(start_range, end_range):
                cols_arr_list.append(i)
        else:
            try:
                #start_range = int(cols) - 1
                #end_range = start_range + 1
                cols_arr_list.append(int(cols) - 1)
            except:
                continue
    for r in inrows:
        newpart = list()
        for i in cols_arr_list:
            if i >= len(r):
                continue
            newpart.append(r[i])
        to_geocode_cols_arr[cols_arr_i].append(newpart)

if not os.path.exists(DIR):
    os.makedirs(DIR)

for geocode_i in range(len(to_geocode_cols_arr[0])):
    if geocode_i == 0:
        continue
    #id = re.sub(r"[ ,]+", "-", "-".join(to_geocode_cols_arr[0][geocode_i]))
    id = "-".join(to_geocode_cols_arr[0][geocode_i])
    fileout = DIR + "/" + id + ".json"
    if os.path.isfile(fileout):
        continue
    geolist = list()
    for x in to_geocode_cols_arr[1][geocode_i]:
        geolist.append(x.strip(" ,"))
    geo = ", ".join(geolist).strip(" ,")
    query_str_dict = geocoding_api_default_args
    query_str_dict["address"] = geo
    query_str = urllib.urlencode(geocoding_api_default_args)
    url_to_fetch = GEOCODING_URL + "?" + query_str
    print "geocode_i: %s" % geocode_i
    print url_to_fetch
    time.sleep(.25)
    f = urllib.urlopen(url_to_fetch)
    print fileout
    out = f.read()
    js = json.loads(out)
    if js["status"] == "OVER_QUERY_LIMIT":
        print "LIMIT REACHED AT %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        time.sleep(86400)
        f = urllib.urlopen(url_to_fetch)
        js = json.loads(out)
    fo = open(fileout, "w")
    fo.write(out)
