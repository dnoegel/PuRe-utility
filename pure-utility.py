#! /usr/bin/env python2
# coding:utf-8

import sys
import os

import shlex
import re
import subprocess

import argparse

"""
Dependencies:
 * pulseaudio
 * mp3splt (optional)
"""

## Prints a table
def print_table(table, padding=0, alignments=None, highlight_first_row=True, grid=True):
    
    ## Get the required width of each column in the table
    col_widths = [max(len(str(row[idx])) for row in table) for idx, x in enumerate(table[0])]
    
    ## Define how which column will be aligned
    # < = align left
    # > = align right
    # = = align center
    # e.g.: ["<", "^", ">"] will align the first column left, the
    # second column centered and the third one right
    # The alignments-list needs to be exactly as long as the total 
    # number of columns in your table.
    if alignments is None:
        alignments = len(col_widths)*"^".split()
    
    for row_index, row in enumerate(table):
        for col, cell in enumerate(row):
            if row_index == 0 and highlight_first_row:
                print "{padding}{content:^{width}}{padding}".format(content=cell, width=col_widths[col], padding=padding*" "),
                if grid and col<len(col_widths)-1:
                    print "|", 
            else:
                print "{padding}{content:{align}{width}}{padding}".format(content=cell, width=col_widths[col], align=alignments[col], padding=padding*" "),
                if grid and col<len(col_widths)-1:
                    print "|", 
        if row_index == 0 and highlight_first_row:
            print
            line = (sum([i+2*(padding+1) for i in col_widths]))*"-"
            line = list(line)
            if grid:
                pos = 0
                for i in col_widths:
                    pos += i+((padding+1)*2)+1
                    try:
                        line[pos-2] = "+"
                    except IndexError:
                        pass
                print "".join(line)
            else:
                print "".join(line)
        else:
            print

def list_sinks():
    """List sinks"""
    sinks = subprocess.check_output(["pacmd", "list-sinks"])
    
    rg = re.compile(r"index: ([0-9]+)[\s\n\r]*name: <([0-9A-Za-z_.\-]+)>", re.M)
    return rg.findall(sinks)

def list_sink_inputs():
    """List input streams"""
    sinks = subprocess.check_output(["pacmd", "list-sink-inputs"])
    
    rg = re.compile(r"index: ([0-9]+).*?sink: ([0-9]+) <(.*?)>.*?media.name = \"(.*?)\".*?application.name = \"(.+?)\"", re.M|re.I|re.S)
    return rg.findall(sinks)

def create_sink(name):
    """create a new fake sink"""
    for idx, sname in list_sinks():
        if sname == name:
            print "There is already a sink with the name '{name}'".format(name=name)
            raise Exception
    cmd = shlex.split("pactl load-module module-null-sink sink_name={name}".format(name=name))
    ret = subprocess.check_output(cmd)
    return ret

def move_sink_input(input_idx, sink_name):
    """move a input to a given sink"""
    if not sink_name in [i[1] for i in list_sinks()]:
        print "There is no sink named '{0}'".format(sink_name)
        raise Exception
    if not input_idx in [i[0] for i in list_sink_inputs()]:
        print "There is no input-index '{0}'".format(input_idx)
        raise Exception
        
    cmd = shlex.split("pactl move-sink-input {index} {name}".format(index=input_idx, name=sink_name))
    
    
    return subprocess.check_output(cmd)


def record(sink_name):
    """record a given sink"""
    if not sink_name in [i[1] for i in list_sinks()]:
        print "There is no sink named '{0}'".format(sink_name)
        raise Exception
    
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    i = 0
    name_scheme = "out{num}.mp3"
    current_name = name_scheme.format(num=i)
    while os.path.exists(os.path.join(path, current_name)):
        i+=1
        current_name = name_scheme.format(num=i)
    
    print "Recording '{0}'".format(current_name)
    cmd = "parec -d {sink_name}.monitor | lame -b 192 -r - {filename}".format(sink_name=sink_name, filename=os.path.join(path, current_name))
    print cmd
    subprocess.call(cmd, shell=True)
    
def split(filename, min, num=None):
    """split a given file"""
    if num:
        cmd = "mp3splt -s -p trackmin={min},nt={num},rm {filename}".format(min=min, num=num, filename=filename)
    else:
        cmd = "mp3splt -s -p trackmin={min},nt=rm {filename},min=120".format(min=min, filename=filename)
        
    if not os.path.exists(filename):
        raise Exception("File '{0}' not found".format(filename))
    
    print "Splitting file"
    print cmd
    subprocess.call(shlex.split(cmd))
    
def cddb(filename):
    """split a given file"""
    #~ cmd = "mp3splt -ac query[search=cddb_cgi://freedb2.org/~cddb/cddb.cgi:80]{{}} {filename}".format(filename=filename)
    #~ if "--musicbrainz" in sys.argv:
        #~ cmd = "mp3splt -ac query[search=cddb_cgi://freedb.musicbrainz.org:80/~cddb/cddb.cgi,get=cddb_cgi://freedb.musicbrainz.org:80/~cddb/cddb.cgi]{{}} {filename}".format(filename=filename)
    #~ else:
    cmd = "mp3splt -ac query{{}} {filename}".format(filename=filename)
        #
    if not os.path.exists(filename):
        raise Exception("File '{0}' not found".format(filename))
    
    print "Splitting file"
    print cmd
    subprocess.call(shlex.split(cmd))

def cue(filename, cue):
    cmd = "mp3splt -ac {cue} {filename}".format(filename=filename, cue=cue)
        #
    if not os.path.exists(filename):
        raise Exception("File '{0}' not found".format(filename))
    if not os.path.exists(cue):
        raise Exception("File '{0}' not found".format(cue))
    
    print "Splitting file"
    print cmd
    subprocess.call(shlex.split(cmd))


parser = argparse.ArgumentParser(description='PuRe - Pulse Record Utility')
group = parser.add_argument_group('List Options')
group.add_argument("-s","--list-sinks", dest="list_sinks", help='List available sinks', action="store_true")
group.add_argument("-i", "--list-sink-inputs", dest="list_sink_inputs", help='List available sink inputs', action="store_true")
group = parser.add_argument_group('Modifying Sinks')
group.add_argument( "-c", "--create",dest="create", help='Create new sink SINK_NAME', metavar="SINK_NAME")
group.add_argument( "-m", "--move",dest="move", help='Move sink input with INPUT_INDEX to sink SINK_NAME', nargs=2, metavar=('INPUT_INDEX','SINK_NAME'))
group = parser.add_argument_group('Record')
group.add_argument( "-r", "--record",dest="record", help='Record a given sink', metavar="SINK_NAME")
group = parser.add_argument_group('Split Options')
group.add_argument( "-d", "--split-detect",dest="split", help='Split a given file FILE into NUMBER parts by detecting silence. Each parts must be at least SECONDS seconds long', nargs=3, metavar=('FILE', "SECONDS", 'NUMBER'))
group.add_argument( "--cddb",dest="cddb", help='Split a given file FILE with some cddb data', metavar="FILE")
group.add_argument( "--cue",dest="cue", help='Split FILE by a given CUE sheet', nargs=2, metavar=("FILE", "CUE"))
args = parser.parse_args()

if not args.list_sinks and not args.list_sink_inputs and not args.create and not args.move and not args.record and not args.split and not args.cddb and not args.cue:
    parser.print_help()
    sys.exit(0)

if args.split and args.cddb:
    raise Exception("CDDB-Split and Silence-Split are mutualy exclusive")

if args.list_sinks:
    print "Available sinks:\n"
    rows = [("Index", "Name")]
    for index, name in list_sinks():
        rows.append((index, name))
    print_table(rows)
if args.list_sink_inputs:
    print "Available sink inputs:\n"
    rows = [("Input ID", "Sink ID", "Sink Name", "Media Name", "Application Name")]
    for index, sink_id, sink_name, media_name, application_name in list_sink_inputs():
        rows.append((index, sink_id, sink_name, media_name, application_name, ))
    print_table(rows)
if args.create:
    print create_sink(args.create)
if args.move:
    print move_sink_input(args.move[0], args.move[1])
    print """You can now run

parec -d {name}.monitor | oggenc -b 192 -o out.ogg --raw -

or

parec -d {name}.monitor | lame -b 192 -r - out.mp3

in order to record the stream. You can also use this script's "record" option.""".format(name=args.move[1])
if args.record:
    record(args.record)
if args.split:
    split(*args.split)
if args.cddb:
    cddb(args.cddb)
if args.cue:
    cue(*args.cue)
