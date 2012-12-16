#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib2, html5lib

def htmltree(url):
    r = urllib2.Request(url)
    r.add_header("User-Agent", "Mozilla/5.0")
    f = urllib2.urlopen(r)
    return f

def webpage(f):
    page = html5lib.HTMLParser(\
        tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
        namespaceHTMLElements=False)
    p = page.parse(f)
    return p

def text(p, x):
    elem = p.xpath(x)[0]
    e = list(elem.itertext())
    return e
