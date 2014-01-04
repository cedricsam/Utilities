#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import argparse

ap = argparse.ArgumentParser(description='Get columns in CSV file.')
ap.add_argument('cols', nargs='?', default=None)
ap.add_argument('infile', nargs='?', type=argparse.FileType('r'), const=sys.stdin, default=sys.stdin)
ap.add_argument('outfile', nargs='?', type=argparse.FileType('a'), const=sys.stdout, default=sys.stdout)
args = ap.parse_args()

cols_arr = args.cols.split(",")

cr = csv.reader(args.infile)
inrows = list()
outrows = list()
for r in cr:
    inrows.append(r)
    outrows.append(list())

for cols in cols_arr:
    if "-" in cols:
        range_cols = cols.split("-")
        try:
            start_range = int(range_cols[0])-1
            end_range = int(range_cols[1])
        except:
            continue
    else:
        try:
            start_range = int(cols) - 1
            end_range = start_range + 1
        except:
            continue
    for i in range(start_range,end_range):
        count = 0
        for r in inrows:
            if i >= len(r):
                continue
            outrows[count].append(r[i])
            count += 1

cw = csv.writer(args.outfile)
cw.writerows(outrows)
