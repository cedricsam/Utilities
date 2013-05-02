#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from decimal import *
import csv
import datetime
import re
import types

if len(sys.argv) <= 3:
    print "Usage: json2csv.py [input file] [base entity] [cols] [opt: numcols]"
    sys.exit()

base = sys.argv[2].split("~")
cols = sys.argv[3].split(",")
if len(sys.argv) > 4:
    numcols = sys.argv[4].split(",")
else:
    numcols = list()
#dateformatin = "%d/%m/%Y %I:%M:%S %p"
#dateformatout = "%Y-%m-%d %H:%M:%S"
cols_lower = list()

for c in cols:
    cols_lower.append(c.lower().replace("~","_"))

# Define IO files
fname = sys.argv[1]
fname_out = re.sub(r"json/", r"csv/", re.sub(r"\.json$", ".csv", fname))
if ".csv" not in fname_out or fname == fname_out:
    fname_out += ".csv"
try:
    f = open(fname, "r")
except IOError as ioe:
    print str(ioe)
    sys.exit()

js = json.loads(f.read())

# Iterate through results
out = list()
el = js
for x in base:
    if re.search(r"[0-9]", x, len(x)-1) is not None:
        n = int(x[len(x)-1:len(x)])-1
        k = x[0:len(x)-1]
        if k not in el:
            el = None
            break
        if (len(el[k])>n):
            el = el[k][n]
        else:
            el = None
    else:
        if el is None:
            break
        if x in el:
            el = el[x]
        else:
            el = None
            break
if el is None:
    sys.exit()
if type(el) is not types.ListType:
    el = [el]

for x in el:
    r = dict()
    for A in cols:
        aa = A.split("~")
        val = x
        for a in aa:
            if re.search(r"[0-9]", a, len(a)-1) is not None:
                n = int(a[len(a)-1:len(a)])-1
                k = a[0:len(a)-1]
                if n == -1:
                    val = len(val[k])
                    break
                if k not in val:
                    val = None
                    break
                if (len(val[k])>n):
                    val = val[k][n]
                else:
                    val = None
            else:
                if val is None:
                    break
                if a in val:
                    val = val[a]
                else:
                    val = None
                    break
        if a in numcols and val is not None:
            val = re.sub(r"[ ,\$a-zA-Z_]+", "", val)
        #if a in datecols and val is not None:
        #    val = datetime.datetime.strptime(val, dateformatin).strftime(dateformatout)
        if val is not None:
            try:
                val = val.encode("utf8")
            except Exception as e:
                pass
        r[A.lower().replace("~","_")] = val
    out.append(r)

#f_out = open(fname_out, "w")
cw = csv.DictWriter(sys.stdout, cols_lower)
#cw.writeheader()
cw.writerows(out)
#fout = open(out)
