#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import html5lib
import json
import os
import traceback

import requests

HEADERS = {
    'Referer': 'http://likms.assembly.go.kr/bill/jsp/BillSearchResult.jsp',
}

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
        r = requests.get(url, headers=HEADERS, stream=True)
        assert r.ok
    except Exception as e:
        import sys
        traceback.print_exc(file=sys.stdout)
        return

    with open(outp, 'wb') as f:
        for block in r.iter_content(1024):
            if not block:
                break
            f.write(block)

def get_webpage_text(url):
    r = requests.get(url, headers=HEADERS)
    return r.text

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

