#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2
import json

try:
    method = str(sys.argv[1].upper())
except:
    print "ftapi.py [method] [data]"
    sys.exit()

sql = sys.argv[2]

params = { "sql": sql }
if len(sys.argv) > 3:
    if sys.argv[3] == "csv":
        params["alt"] = "csv"

url = "https://www.googleapis.com/fusiontables/v1/query"

f_token = open("/home/csam/google.fusiontables.token", "r")
token_txt = f_token.read()
token = json.loads(token_txt)

headers = { "Authorization": token["token_type"] + " " + token["access_token"], "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain" }

if method == "GET":
    #print url + "?%s" % urllib.urlencode(params)
    url += "?" + urllib.urlencode(params)
    req = urllib2.Request(url, headers=headers)
else:
    #print url
    req = urllib2.Request(url, data=urllib.urlencode(params), headers=headers)
req.get_method = lambda: method
resp = urllib2.urlopen(req)
resp_txt = resp.read()

print resp_txt
