#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import pprint

if len(sys.argv) < 2:
    print "Missing file"
    sys.exit()

f = open(sys.argv[1], "r")

js = json.loads(f.read())

pp = pprint.PrettyPrinter(indent=4)

print pp.pprint(js)
