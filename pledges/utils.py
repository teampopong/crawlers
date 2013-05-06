#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import html5lib
import urllib2

def get_webpage(url, outp, decoding=None):
    r = urllib2.urlopen(url)
    with open(outp, 'w') as f:
        if decoding==None:
            f.write(r.read())
        else:
            f.write(r.read().decode(decoding))

def read_webpage(filename):
    with open(filename) as f:
        page = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)
        p = page.parse(f, encoding='utf-8')
    return p

def find_pledge(filename, x):
    page = read_webpage(filename)
    elems = page.xpath(x)
    return [list(elem.itertext()) for elem in elems]
