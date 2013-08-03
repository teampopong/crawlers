#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import re
import html5lib

def get_webpage(f):
    page = html5lib.HTMLParser(\
        tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
        namespaceHTMLElements=False)
    p = page.parse(f)
    return p

def get_element_texts(p, x):
    elems = p.xpath(x)
    return (list(elem.itertext()) for elem in elems)

def parse(directory, filename, rng=(1, 4)):

    d = {}
    for i in range(rng[0], rng[1]+1):

        fn = '%s/%d.html' % (directory, i)
        with open(fn, 'r') as f:
            page = get_webpage(f)

        if i==2:
            x_term = '//td[@colspan="2"]/text()'
            x_expl = '//td[@width="15"]/following-sibling::td'

            terms = [re.split(r'[().]', p)\
                    for p in page.xpath(x_term) if '(' in p]
            expls = ['\n'.join(\
                    filter(None, (e.strip()\
                        .replace(unichr(int('201C', 16)), '\'')\
                        .replace(unichr(int('201D', 16)), '\'')\
                        for e in expl)))\
                    for expl in get_element_texts(page, x_expl)]

            for t in terms:
                term = t[1].strip()
                d[term] = [e for e in expls if term in e][0]
        if i==4:
            x_terms = '//td[@width="15"]/following-sibling::td'
            items = filter(None, (\
                    t.strip() for t in page.xpath('//text()') if u'▷' in t))
            terms = [filter(None, re.split(ur'[▷：:]', t)) for t in items]

            for t, e in terms:
                d[t.strip()] = e.strip()
        else:
            pass

    with open(filename, 'w') as f:
        f.write('"ko","kodesc"\n')
        for t, e in d.items():
            s = '"%s","%s"\n' % (t, e)
            f.write(s.encode('utf-8'))
    print 'Data written to ' + filename

    return d
