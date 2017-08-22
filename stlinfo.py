#! /usr/bin/env python3
# vim:fileencoding=utf-8
#
# Copyright © 2012-2017 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Last modified: 2017-08-20 18:06:21 +0200
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
"""
Read an STL file and print information about the object.

Optionally print a text representation of the object. It can also write a binary
STL version of the object.
"""

import argparse
import logging
import sys
import time
from stltools import stl, bbox, utils

__version__ = '5.0.0'


def main(argv):
    """
    Entry point for stlinfo.

    Arguments:
        argv: command line arguments (without program name!)
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-t',
        '--text',
        action='store_true',
        help='print text representation of the file')
    parser.add_argument(
        '-b',
        '--binary',
        action='store_true',
        help='write binary representation of the file')
    parser.add_argument(
        '-v', '--version', action='version', version=__version__)
    parser.add_argument(
        '--log',
        default='warning',
        choices=['debug', 'info', 'warning', 'error'],
        help="logging level (defaults to 'warning')")
    parser.add_argument('file', nargs='*', help='one or more file names')
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=getattr(logging, args.log.upper(), None),
        format='%(levelname)s: %(message)s')
    if not args.file:
        parser.print_help()
        sys.exit(0)
    for fn in args.file:
        if not fn.lower().endswith('.stl'):
            w = 'The file "{}" is probably not an STL file, skipping.'
            logging.warning(w.format(fn))
            continue
        try:
            vertices, name = stl.readstl(fn)
            if args.text or args.binary:
                facets, points = stl.toindexed(vertices)
                normals, vectors = stl.normals(facets, points)
        except ValueError as e:
            logging.error('{}: {}'.format(fn, e))
            continue
        print("# Information for:", fn)
        print("# Generated by stlinfo {}".format(__version__))
        print("# on {}.".format(time.asctime()))
        print('# Name: "{}"'.format(name))
        print('# Number of facets: {:.0f}'.format(len(vertices) / 3))
        minx, maxx, miny, maxy, minz, maxz = bbox.makebb(vertices)
        print('# Bounding box:')
        print('#   {} ≤ x ≤ {}'.format(minx, maxx))
        print('#   {} ≤ y ≤ {}'.format(miny, maxy))
        print('#   {} ≤ z ≤ {}'.format(minz, maxz))
        if args.text:
            print('# Text representation:')
            print(stl.text(name, facets, points, normals, vectors))
        if args.binary:
            on = utils.outname(fn, '.stl', '_bin')
            print('# Writing binary represtation to "{}".'.format(on))
            with open(on, 'w+b') as of:
                of.write(stl.binary(name, facets, points, normals, vectors))


if __name__ == '__main__':
    main(sys.argv[1:])
