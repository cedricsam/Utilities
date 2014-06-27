#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import datetime
import urllib
import urllib2
import smtplib
from xml.dom import minidom

try:
    key = str(sys.argv[1])
    worksheet_id = str(sys.argv[2])
except:
    print "Missing Key or Worksheet ID"
    sys.exit()

numeric_cols = ["lat", "lng"]
integer_cols = ["zoom"]

f_token = open("/home/csam/google.spreadsheets.token", "r")
token_txt = f_token.read()
token = json.loads(token_txt)
f_token.close()

headers = { "Authorization": token["token_type"] + " " + token["access_token"] }
url = "https://spreadsheets.google.com/feeds/list/%(key)s/%(worksheet_id)s/private/full" % { "key": key, "worksheet_id": worksheet_id }
request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)
spreadsheet = response.read()

#print spreadsheet

try:
    dom = minidom.parseString(spreadsheet)
except Exception as e:
    print e
    sys.exit()

entries = list()
for entry in dom.getElementsByTagName('entry'):
    row = dict()
    for cell in entry.childNodes:
	if cell.tagName.startswith("gsx:"):
	    row_tag = cell.tagName.split(":")[1]
	    try:
		if row_tag in numeric_cols:
		    row[row_tag] = float(cell.firstChild.nodeValue)
		elif row_tag in integer_cols:
		    row[row_tag] = int(cell.firstChild.nodeValue)
		elif row_tag.startswith("is-"):
		    row_tag = row_tag[3:len(row_tag)]
		    val = cell.firstChild.nodeValue
		    if val is not None:
			if val.lower() in ["no", "false", "0"]:
			    row[row_tag] = False
			else:
			    row[row_tag] = True
		    else:
			row[row_tag] = None
		else:
		    row[row_tag] = cell.firstChild.nodeValue
	    except:
		pass
    entries.append(row)

print json.dumps(entries)
