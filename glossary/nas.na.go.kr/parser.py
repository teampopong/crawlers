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
    return ['"%s","%s","",""' % (i[1], i[3].strip()) for i in e[1:]]

if __name__=='__main__':

    directory = 'html'
    npage = 126
    outf = 'data.csv'
    x = '//table[@class="cboard"]//tr'

    with open(outf, 'a') as f:
        for i in range(1, npage+1):
            inf = '%s/%s.html' % (directory, i)
            f.write('\n'.join(get_text(inf, x)).encode('utf-8'))
            f.write('\n')
            print '%s/%s' % (i, npage)
