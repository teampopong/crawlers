#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import html5lib

def get_webpage(f):
    page = html5lib.HTMLParser(\
        tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
        namespaceHTMLElements=False)
    p = page.parse(f)
    return p

def get_elements(p, x):
    elems = p.xpath(x)
    e = [list(elem.itertext()) for elem in elems]
    return e

def get_text(inf, x):
    with open(inf, 'r') as f:
        p = get_webpage(f)
        e = p.xpath(x)[1:]
    names = [i.xpath('text()')[0] for i in e]
    urls = [i.xpath('@href')[0] for i in e]
    return ['"%s","%s"' % (n, u) for n, u in zip(names, urls)]

def parse(directory, filename, rng=None):
    x = '//ul[@class="inn"]//li/node()'

    with open(filename, 'wa') as f:
        f.write('"ko","kodesc"\n')
        inf = '%s/1.html' % directory
        rows = get_text(inf, x)
        f.write('\n'.join(get_text(inf, x)).encode('utf-8'))
        f.write('\n')
        print 'parsed %s' % inf

    print 'Results written to ' + filename
