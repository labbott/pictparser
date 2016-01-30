#!/usr/bin/env python

import os
import re
import struct
import sys
import subprocess

if len(sys.argv) < 2:
    print "Usage: "+sys.argv[0]+": <path to file>"
    sys.exit(1)

p = subprocess.Popen(["DeRez", "-only", "PICT", sys.argv[1]], \
			stdout=subprocess.PIPE,\
			stderr=subprocess.PIPE)
out, err = p.communicate()
out = out.split('\n')
for l in out:
    if len(l) == 1:
        continue
    # start of file
    if re.match('data \'PICT\'', l):
        m = re.search('\d\d\d\d', l)
        num = m.group(0)
        print "open "+num
        working = open("res"+num+".pct", "wb")
        for a in range(0, 512):
            s = struct.pack(">B", 0);
            working.write(s)
    # end of file
    elif re.match('\}\;', l):
        working.close()
        print "done"
    # file data
    else:
        cap = re.search('\".*\" ', l)
        if cap is None:
            continue
        data = cap.group(0)
        data = data.translate(None, '"')
        for a in data.split(' '):
            if len(a) != 4:
                continue
            first, second = a[:len(a)/2], a[len(a)/2:]
            pdata = struct.pack(">BB", int(first, 16), int(second, 16))
            working.write(pdata)
