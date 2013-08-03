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
        e = get_elements(p, x)
    return ['"%s","%s"' % (i[1], i[3].strip()) for i in e[1:]]

def parse(directory, filename, rng=(1, 126)):
    x = '//table[@class="cboard"]//tr'

    with open(filename, 'wa') as f:
        f.write('"ko","en"\n')
        for i in range(rng[0], rng[1]+1):
            inf = '%s/%s.html' % (directory, i)
            f.write('\n'.join(get_text(inf, x)).encode('utf-8'))
            f.write('\n')
            print 'parsed %s/%s' % (i, rng[1])

    print 'Results written to ' + filename
