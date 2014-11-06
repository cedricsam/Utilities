#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import json
import datetime
import urllib
import urllib2
import smtplib
from xml.dom import minidom

try:
    ftid = str(sys.argv[1])
except:
    print "Missing Fusion Tables ID"
    sys.exit()

numeric_cols = ["lat", "lng"]
integer_cols = ["zoom"]

f_token = open("/home/csam/google.fusiontables.token", "r")
token_txt = f_token.read()
token = json.loads(token_txt)
f_token.close()

headers = { "Authorization": token["token_type"] + " " + token["access_token"] }
url = "https://www.googleapis.com/fusiontables/v1/query?sql=SELECT%%20*%%20FROM%%20%(ftid)s" % { "ftid": ftid }
request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)
data = response.read()

#print spreadsheet

keys = list()

try:
    js = json.loads(data)
except Exception as e:
    print e
    sys.exit()

if "columns" not in js:
    print js
    sys.exit()

cw = csv.writer(sys.stdout)
cw.writerow(js["columns"])
for row in js["rows"]:
    try:
        newrow = list()
        for x in row:
            x = x.encode("utf8")
            newrow.append(x)
        cw.writerow(newrow)
    except Exception as e:
        print(str(e),sys.stderr)
        continue
