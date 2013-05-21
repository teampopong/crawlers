#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import meta
import specific

s, e = 18, 18

def get_meta(a, n):
    print '## Get meta data'
    n = meta.get_npages(a)
    meta.get_html(a, n)
    meta.html2csv(a, n)

def get_specific():
    print '## Get specific data'
    specific.get_html()
    specific.html2json()

for a in range(s, e+1):
    print '\n# Assembly %d' % a
    #get_meta(a, n)
    get_specific()
