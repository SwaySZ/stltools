#! /usr/bin/env python
# -*- python coding: utf-8 -*-
# Copyright © 2012,2013 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# $Date$
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

'''Reads an STL file and prints information about the object or a text
representation of the object in the file.'''

import argparse
import sys
import time
from brep import stl, bbox


ver = ('stlinfo [ver. ' + '$Revision$'[11:-2] + 
       '] ('+'$Date$'[7:17]+')')


def main(argv):
    """Main program.

    Keyword arguments:
    argv -- command line arguments (without program name!)
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--text', action='store_true',
                        help='print text representation of the file')
    parser.add_argument('file', nargs='*', help='one or more file names')
    args = parser.parse_args(argv)
    if not args.file:
        parser.print_help()
        sys.exit(0)
    for fn in args.file:
        try:
            facets, points, name = stl.readstl(fn)
            if args.text:
                normals, vectors = stl.normals(facets, points)
        except ValueError as e:
            print fn + ':', e
            sys.exit(1)
        print "# Information for:", fn
        print "# Generated by {}\n# on {}.".format(ver, time.asctime())
        print '# Name: "{}"'.format(name)
        print '# Number of facets:', len(facets)
        print '# Number of unique vertices:', len(points)
        minx, maxx, miny, maxy, minz, maxz = bbox.makebb(points)
        print '# Bounding box:'
        print '#   {} ≤ x ≤ {}'.format(minx, maxx)
        print '#   {} ≤ y ≤ {}'.format(miny, maxy)
        print '#   {} ≤ z ≤ {}'.format(minz, maxz)
        if args.text:
            print "# Text representation:"
            print stl.text(name, facets, points, normals, vectors)


if __name__ == '__main__':
    main(sys.argv[1:])
