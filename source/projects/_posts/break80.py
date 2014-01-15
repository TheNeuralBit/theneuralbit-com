#! /usr/bin/env python

import sys

infile  = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')

for line in infile.read().split('\n'):
    while len(line) > 80:
        idx = line[:80].rfind(' ')
        outfile.write('%s\n' % line[:idx])
        line = line[idx + 1:]
    outfile.write('%s\n' % line)
