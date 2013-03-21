#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import html5lib
import urllib2
import json
from pprint import pprint

settings  = {
        'USER_AGENT': "Mozilla/5.0",
        'N_COLUMNS': 6,
        'HEADERS': ['hangul', 'hanja', 'revised', 'mr', 'others', 'freq'],
        'X_PATH': "//div[@id='mw-content-text']/table/tbody/tr"
        }

URL = '''http://en.wikipedia.org/w/index.php?title=List_of_Korean_family_names'''

def getlastnames(url=URL):
    xpaths = getxpaths(url)
    printjson('lastnames.json', xpaths)
    #l = list(chunklist(table, settings["N_COLUMNS"]))
    return xpaths

def getxpaths(url=URL):
    p = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)
    r = urllib2.Request(url)
    r.add_header("User-Agent", settings["USER_AGENT"])
    f = urllib2.urlopen(r)

    page = p.parse(f)
    xpaths = page.xpath(settings["X_PATH"])

    return xpaths

def printjson(filename, xpaths):
    data = []

    for xpath in xpaths:
        data.append(dict(zip(settings["HEADERS"], xpath.xpath('td/text()'))))

    with open(filename, 'w') as f:
        json.dump(data, f,  encoding="UTF-8", indent=2)

def chunklist(l, n):
    for i in range(0, len(l), n):
        yield table[i:i+n]

if __name__ == '__main__':
    getlastnames(URL)
