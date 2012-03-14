#!/usr/bin/env python2
# coding:utf-8

import os
import sys
import math
content = []
with open("labels.txt") as fh:
    for line in fh:
        content.append(line.split())
    
content = sorted(content, key=lambda k:float(k[0].replace(",", ".")))

header = """TITLE "UNKNOW ALBUM"
PERFORMER "UNKNOWN ARTIST"
FILE "UNKNOWN.FILE" WAVE"""

title = """TRACK {num} AUDIO
    INDEX 01 {index}"""

output = [header]
for num, entry in enumerate(content):
    try:
        start, end, name = entry
    except ValueError:
        start, end = entry
        name = "Unknown"
    start = float(start.replace(",", "."))

    m,s = divmod(start, 60)
    f = (s-math.floor(s))
    idx = ":".join(str(int(i)) for i in (m, s, f))
    
    output.append(title.format(index=idx, num=num+1))

with open("labels.cue", "w") as fh:
    fh.write("\n".join(output))

print "done"
