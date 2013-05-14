#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import html5lib
import urllib2

def get_webpage(url, outp):
    r = urllib2.urlopen(url)
    with open(outp, 'w') as f:
        f.write(r.read())

def read_webpage(filename):
    with open(filename) as f:
        page = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)
        p = page.parse(f)
    return p

def get_elems(page, x):
    return page.xpath(x)

def get_elem_texts(page, x):
    elems = page.xpath(x)
    return [list(elem.itertext()) for elem in elems]
