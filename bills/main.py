#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from getlist import getlist
from parselist import parselist

s = 1
e = 19

for a in range(s, e+1):
    print '\n# Assembly %d' % a
    npages = getlist(a)
    parselist(a, npages)
