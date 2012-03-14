#!/usr/bin/env python2
# coding:utf-8

import os
import sys
import math
import argparse

HEADER = """TITLE "UNKNOW ALBUM"
PERFORMER "UNKNOWN ARTIST"
FILE "UNKNOWN.FILE" WAVE"""

TITLE = """TRACK {num} AUDIO
    INDEX 01 {index}"""
    
def run(filename):
    content = []
    with open(filename) as fh:
        for line in fh:
            content.append(line.split())
        
    content = sorted(content, key=lambda k:float(k[0].replace(",", ".")))

    
    output = [HEADER]
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
        
        output.append(TITLE.format(index=idx, num=num+1))
    
    name, ext = os.path.splitext(filename)
    #~ with open("".join([name, ".cue"]), "w") as fh:
        #~ fh.write("\n".join(output))
    print "\n".join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert an Audacity label-file to a cue file')
    parser.add_argument("-f", "--file", dest="inputfile", help='FILE to convert. Pipe output into new file, if you like to.', metavar="FILE")
    args = parser.parse_args()
    
    if args.inputfile:
        run(args.inputfile)
    else:
        parser.print_help()
