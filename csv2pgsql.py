#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import mypass

if len(sys.argv) < 4:
    print "Usage: csv2pgsql.py [input file] [table name] [columns]"
    sys.exit()

f = open(sys.argv[1], "r")

cols = sys.argv[3].split(",")
id = cols[0]

cr = csv.DictReader(f, cols)

conn = mypass.getConn()

for r in cr:
    try:
        r["dbinserted"] = "NOW()"
        conn.insert(sys.argv[2], r)
    except Exception as e:
        continue
        try:
            del r["dbinserted"]
            r["dbupdated"] = "NOW()"
            conn.update(sys.argv[2], r)
        except Exception as e:
            #print str(e)
            continue
        print str(e)

f.close()

