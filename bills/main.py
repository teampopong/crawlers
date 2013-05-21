#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from meta import get_npages, get_html, html2csv


s, e = 1, 1

for a in range(s, e+1):

    print '\n# Assembly %d' % a

    print '## Get meta data'
    n = get_npages(a)
    get_html(a, n)
    html2csv(a, n)
