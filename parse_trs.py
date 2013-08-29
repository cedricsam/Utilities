#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import csv
import datetime
from bs4 import BeautifulSoup
import types

out = sys.stdout

if len(sys.argv) <= 1:
    sys.exit()
classes = None
if len(sys.argv) > 2:
    classes = sys.argv[2]

f = open(sys.argv[1], "r")
intext = f.read()
soup = BeautifulSoup(intext)

cw = csv.writer(out)
filename = sys.argv[1].split("/")[len(sys.argv[1].split("/"))-1]
if "." in filename:
    shortfilename = ".".join(filename.split(".")[0:len(filename.split("."))-1])
else:
    shortfilename = filename

if classes is None:
    trs = soup.find_all("tr")
else:
    trs = soup.select("table."+(classes.replace(" ","."))+" tr")
for tr in trs:
    r = list()
    if tr is None:
        continue
    tds = tr.find_all("td")
    if len(tds) <= 0:
        continue
    #r.append(soup.find("input", id="hiddenSeasonOption").get("value"))
    #r.append(tds[1].find("a").get("href").replace("/ice/player.htm?id=",""))
    r.append(shortfilename)
    for td in tds:
        children_length = len(list(td.children))
        if children_length > 1:
            for tdc in td.children:
                try:
                    tagname = tdc.name
                    if tagname == "a":
                        r.append(re.sub("\s+", " ", tdc.get("href").strip("\n ")))
                except:
                    pass
                try:
                    r.append(re.sub("\s+", " ", tdc.string.strip("\n ")))
                except:
                    r.append("")
            #for ss in td.strings:
            #    r.append(re.sub("\s+", " ", ss.strip("\n ")))
        else:
            r.append(re.sub(r"\s+", " ", td.text.strip("\n ")))
    for i in range(len(r)):
        try:
            r[i] = r[i].encode("utf8")
        except:
            pass
        if r[i] is not None and "," in r[i]:
            try:
                r[i] = re.sub(r"([0-9]),([0-9]{3})",r"\1\2",r[i])
            except:
                pass
        try:
            r[i] = r[i].strip()
            if r[i] == "-":
                r[i] = None
        except Exception as e:
            pass
    cw.writerow(r)

