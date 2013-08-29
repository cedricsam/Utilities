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
#r = pgconn.get_attnames(tablename)
sql = "select column_name, udt_name from information_schema.columns WHERE table_name = '%s' order by ordinal_position" % tablename
res = pgconn.query(sql).getresult()

out = {
    "kind": "fusiontables#table",
    "name": tablename,
    "columns": [
    ],
    "description": description,
    "isExportable": False,
    "attribution": "Cédric Sam",
    "attributionLink": "http://cedric.sam.name/"
}
i = 0
#print res
for r in res:
    k = r[0]
    v = r[1]
    if v in ["numeric"] or v.startswith("int"):
        typ = "NUMBER"
    elif v in ["date"] or v.startswith("time"):
        typ = "DATETIME"
    elif v in ["varchar"]:
        typ = "STRING"
    elif v in ["geometry"] or k in ["lat", "lng", "latitude", "longitude", "kml", "bounds", "point"]:
        typ = "LOCATION"
    else:
        typ = "STRING"
    col = { "columnId": i, "name": k, "type": typ }
    i += 1
    out["columns"].append(col)

print json.dumps(out)
