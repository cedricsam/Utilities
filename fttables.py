#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pg
import json
import mypass
import types

if len(sys.argv) < 2:
    print "Missing table name"
    sys.exit()

tablename = sys.argv[1]
description = ""
if len(sys.argv) > 2:
    description = sys.argv[2]
pgconn = mypass.getConn()
#r = pgconn.query("SELECT * FROM %s LIMIT 1" % tablename).dictresult()
r = pgconn.get_attnames(tablename)

out = {
    "kind": "fusiontables#table",
    "name": tablename,
    "columns": [
    ],
    "description": description,
    "isExportable": False,
    "attribution": "Cedric Sam",
    "attributionLink": "http://cedric.sam.name/"
}
i = 0
for k in r.keys():
    v = r[k]
    if v in ["num", "int"]:
        typ = "NUMBER"
    elif v in ["date"]:
        typ = "DATETIME"
    elif v in ["text"]:
        typ = "STRING"
    elif k in ["the_geom", "geometry", "point", "boundary", "geo"]:
        typ = "LOCATION"
    else:
        typ = "STRING"
    col = { "columnId": i, "name": k, "type": typ }
    i += 1
    out["columns"].append(col)

print json.dumps(out)
