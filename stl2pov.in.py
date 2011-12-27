#! /usr/bin/env python
# -*- python coding: utf-8 -*-
# Copyright © 2011 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <2011-12-22 22:40:18 rsmith>
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

'''Program for converting an STL file into a POV-ray mesh.'''

import sys
import os
import string
import time

import stl

ver = "stl2pov [rev. UkZTVkVS] (UkZTREFU)"

def usage():
    print ver
    print "Usage: stl2pov infile [outfile]"

# This is the main program
if len(sys.argv) == 1:
    usage()
    sys.exit(0)
try:
    stlobj = stl.Surface(sys.argv[1])
except:
    print "The file '{}' cannot be read or parsed. Exiting.".format(sys.argv[1])
    sys.exit(1)
# Remove spaces from name
stlobj.name = stlobj.name.strip()
stlobj.name = stlobj.name.translate(string.maketrans(string.whitespace,
                                           "_"*len(string.whitespace)))
# Prepare output string.
outs = "// Generated by {} on {}.\n".format(ver, time.asctime())
outs += stlobj.stats('// ')+'\n'
outs += "// The abovementioned coordinates are in the STL file's right-handed\n"
outs += "// coordinate system, while POV-ray uses a left-handed system.\n"
outs += "// You should swap the x and y above to get POV-ray coordinates.\n"
outs += "# declare m_{} = mesh {{\n".format(stlobj.name)
sot = "  triangle {{ // #{}\n"
fc = "    <{1}, {0}, {2}>,\n"
fct = "    <{1}, {0}, {2}>\n"
for n, f in enumerate(stlobj.facets):
    outs += sot.format(n+1)
    outs += fc.format(f.v[0].x, f.v[0].y, f.v[0].z)
    outs += fc.format(f.v[1].x, f.v[1].y, f.v[1].z)
    outs += fct.format(f.v[2].x, f.v[2].y, f.v[2].z)
    outs += "  }\n"
outs += "}\n"
# Send output.
if len(sys.argv) < 3:
    # Derive output name
    outbase = os.path.basename(sys.argv[1])
    if outbase.endswith((".stl", ".STL")):
        outbase = outbase[:-4]
    outfile = outbase+".inc"
# Or to a named output file.
else:
    outfile = sys.argv[2]
try:
    outf = open(outfile, "w+")
    outf.write(outs)
    outf.close()
except:
    print "Cannot write output file '{}'".format(sys.argv[2])
    sys.exit(2)
