#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import json
import types

if len(sys.argv) < 2:
    print "Missing file"
    sys.exit()

f = open(sys.argv[1], "r")

cr = csv.DictReader(f)

a = []

for r in cr:
    a.append(r)
    for x in r:
        try:
            r[x] = int(r[x])
        except:
            pass

f.close()

out = sys.stdout
#fout = open(out)
out.write(json.dumps(a))
out.close()
