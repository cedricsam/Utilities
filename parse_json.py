#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Generic parser for JSON arrays

import sys
import json
import csv
import types
import argparse

ap = argparse.ArgumentParser(description='Get columns in CSV file.')
ap.add_argument('cols')
ap.add_argument('infile', nargs='?', type=argparse.FileType('r'), const=sys.stdin, default=sys.stdin)
ap.add_argument('outfile', nargs='?', type=argparse.FileType('a'), const=sys.stdout, default=sys.stdout)
ap.add_argument('-sa', '--sub-array', nargs='?', help='Used if the data comes from an array inside each object')
ap.add_argument('-fk', '--foreign-key', nargs='?', help='Key in parent object for sub-array')
ap.add_argument('--headers', dest='headers', action='store_true')
ap.add_argument('--no-headers', dest='headers', action='store_false')
ap.set_defaults(headers=False)

args = ap.parse_args()

cols = args.cols.split(",")
fkeys = []

if len(cols) <= 0:
    sys.exit()

cw = csv.DictWriter(args.outfile, cols)

try:
    js = json.loads(args.infile.read())
except:
    sys.exit()

if args.sub_array is not None:
    if len(js) < 1 or args.sub_array not in js[0]:
        sys.exit()
    if args.foreign_key is not None and len(args.foreign_key) > 0:
        fkeys = args.foreign_key.split(",")
        for fk in reversed(fkeys):
            if fk not in js[0] or fk in cols:
                sys.exit()
            cols.insert(0, fk)

if args.headers:
    cw.writeheader()

for row in js:
    fkvals = {}
    if len(fkeys) > 0:
        for fk in fkeys:
            try:
                fkvals[fk] = row[fk].encode("utf8")
            except:
                fkvals[fk] = row[fk]
    if args.sub_array is not None:
        row = row[args.sub_array]
    else:
        row = [row]
    for rr in row:
        r = {}
        for col in cols:
            if col in fkeys and col in fkvals:
                r[col] = fkvals[col]
            elif col not in rr:
                r[col] = None
            elif col in rr and (type(rr[col]) is types.StringType or type(rr[col]) is types.UnicodeType):
                r[col] = rr[col].encode("utf8")
            else:
                r[col] = rr[col]
        cw.writerow(r)
