#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

if len(sys.argv) < 2:
    print "Missing file"
    sys.exit()

f = open(sys.argv[1])
js = json.loads(f.read())
count = int(js["rows"][0][0])

print count
