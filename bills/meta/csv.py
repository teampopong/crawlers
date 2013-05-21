#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import re
import sys

import lxml
import utils
from settings import DIR, BASEURL, META_HEADERS, X

def parselist(assembly_id, npages):

    def list_to_file(l, f):
        f.write('"')
        f.write('","'.join(l).encode('utf-8'))
        f.write('"\n')

    def parse_columns(columns):
        data = []
        for j, c in enumerate(columns):
            if j==1:
                status = str(int(\
                       re.findall(r'[0-9]+', c.xpath('img/@src')[0])[0]))
                title = c.xpath('a/text()')[0]
                link = re.findall(r'\w+', c.xpath('a/@href')[0])[2]
                data.extend([status, title, link])
            elif j==6:
                data.append('1' if c.xpath('img/@onclick') else '0')
            else:
                data.append(c.xpath('text()')[0].strip())
        return data

    def parse_page(page, f, assembly_id):
        fn = '%s/%s/%d.html' % (DIR['list'], assembly_id, page)
        p = utils.read_webpage(fn)
        rows = utils.get_elems(p, X['table'])

        for r in reversed(rows):
            columns = r.xpath(X['columns'])
            if len(columns)==8:
                p = parse_columns(columns)
                list_to_file(p, f)

        sys.stdout.write('%d\t' % page)
        sys.stdout.flush()

    directory = DIR['meta']
    utils.check_dir(directory)
    meta_data = '%s/%d.csv' % (directory, assembly_id)

    print '\nParsing:'
    with open(meta_data, 'wa') as f:
        list_to_file(META_HEADERS, f)
        for page in range(1, npages+1):
            parse_page(page, f, assembly_id)

    print '\nMeta data written to ' + meta_data
