#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import types

if len(sys.argv) < 2:
    print "Missing file"
    sys.exit()

f = open(sys.argv[1], "r")

recoded_str = u""
added_n = 0
for c in f.read():
    n = ord(c)
    if n in range(128):
        if added_n > 0:
            recoded_str += unichr(added_n + 127)
            added_n = 0
        recoded_str += unichr(n)
    else:
        added_n += n #(n - 128)

print recoded_str.encode("utf8")
