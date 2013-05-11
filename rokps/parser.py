#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import json

import html5lib
import lxml

def get_webpage(inf):
    with open(inf, 'r') as f:
        page = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)
        p = page.parse(f, encoding='euc-kr-8')
    return p

def extract_data(elems):
    d = {}
    for i, e in enumerate(elems):
        if isinstance(e, lxml.etree._Element):
            key = e.xpath(key_x)[0].replace(' ', '')
            d[key] = ''
        else:
            d[key] += '\n' + elems[i].strip()
    return d

def write_data(data, f):
    json.dump(data, f, indent=2)

if __name__=='__main__':

    directory = '/home/e9t/data/popong/people/rokps/html'
    npage = 2810
    outf = 'data.json'
    elem_x = '//table[@width="95%"]//td[@align="left"]/node()[normalize-space()]'
    key_x = 'descendant::text()'

    empty = []

    with open(outf, 'wa') as f:
        f.write('[\n')

        for i in range(1, npage+1):
            try:
                page = get_webpage('%s/%s.html' % (directory, i))
                elems = page.xpath(elem_x)
                data = extract_data(elems)
                write_data(data, f)
                if i < npage:
                    f.write(',\n')
                else:
                    f.write('\n]')
                print '%d written to file' % i

            except IOError, e:
                empty.append(i)
                print '%d is empty' % i

    print empty
