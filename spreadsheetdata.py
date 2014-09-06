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
    key = str(sys.argv[1])
except:
    print "Missing Sheets Key"
    sys.exit()

f_token = open("/home/csam/google.spreadsheets.token", "r")
token_txt = f_token.read()
token = json.loads(token_txt)
f_token.close()

headers = { "Authorization": token["token_type"] + " " + token["access_token"] }
url = "https://spreadsheets.google.com/feeds/worksheets/%(key)s/private/basic" % { "key": key }
request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)
spreadsheet = response.read()

#print spreadsheet

cols = ["id", "title", "updated"]

try:
    dom = minidom.parseString(spreadsheet)
except Exception as e:
    print e
    sys.exit()

entries = list()
for entry in dom.getElementsByTagName('entry'):
    row = dict()
    for cell in entry.childNodes:
	if cell.tagName in cols:
            try:
                row[cell.tagName] = cell.firstChild.nodeValue.encode("utf8")
            except:
                row[cell.tagName] = cell.firstChild.nodeValue
            if cell.tagName == "id":
                row[cell.tagName] = row[cell.tagName].split("/")[len(row[cell.tagName].split("/"))-1]
    entries.append(row)

cw = csv.DictWriter(sys.stdout, cols)
cw.writeheader()
for x in entries:
    try:
        cw.writerow(x)
    except:
        continue
        print(x,sys.stderr)
