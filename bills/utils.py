#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import html5lib
import json
import os
from shutil import copyfileobj
import urllib2

opener = urllib2.build_opener()
opener.addheaders.append(('Referer', 'http://likms.assembly.go.kr/bill/jsp/BillSearchResult.jsp'))

def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_elems(page, x):
    return page.xpath(x)

def get_elem_texts(page, x):
    elems = page.xpath(x)
    return [list(elem.itertext()) for elem in elems]

def get_webpage(url, outp):
    try:
        r = opener.open(url)
    except urllib2.URLError:
        print 'URLError: %s' % url
        return

    with open(outp, 'w') as f:
        copyfileobj(r, f)

def get_webpage_text(url):
    return opener.open(url).read()

def read_json(fname):
    with open(fname, 'r') as f:
        return json.load(f)

def read_webpage(filename):
    with open(filename) as f:
        page = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)
        p = page.parse(f)
    return p

def write_json(data, fn):
    with open(fn, 'w') as f:
        json.dump(data, f, indent=2)
    print 'Data written to ' + fn
