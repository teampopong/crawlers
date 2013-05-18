#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import json
import html5lib
import urllib2
from settings import TERMS

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

def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_terms():
    with open(TERMS, 'r') as f:
        rows = f.read().split('\n')[1:]
        return dict(filter(None,\
                (filter(None,row.decode('utf-8').split(',')) for row in rows)))

def write_json(data, fn):
    with open(fn, 'w') as f:
        json.dump(data, f, indent=2)
    print 'Data written to ' + fn
