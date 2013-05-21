#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import re
import sys

import lxml
import utils
from settings import DIR, BASEURL, META_HEADERS, X

def parselist(assembly_id, npages):

    def extract(columns):
        data = []
        for j, c in enumerate(columns):
            if j==1:
                data.append(str(int(\
                        re.findall(r'[0-9]+', c.xpath('img/@src')[0])[0])))
                data.append(c.xpath('a/text()')[0])
                data.append(re.findall(r'\w+', c.xpath('a/@href')[0])[2])
            elif j==6:
                url = c.xpath('img/@onclick')
                data.append('1' if url else '0')
            else:
                data.append(c.xpath('text()')[0].strip())
        return data

    def get_data(i, f, assembly_id):
        fn = '%s/%s/%s.html' % (DIR['list'], assembly_id, i)
        page = utils.read_webpage(fn)
        rows = utils.get_elems(page, X['table'])

        for r in reversed(rows):
            columns = r.xpath(X['columns'])
            if len(columns)==8:
                f.write('"')
                f.write('","'.join(extract(columns)).encode('utf-8'))
                f.write('"\n')
        sys.stdout.write('%d\t' % i)
        sys.stdout.flush()

    directory = DIR['meta']
    utils.check_dir(directory)
    meta_data = '%s/%d.csv' % (directory, assembly_id)

    with open(meta_data, 'wa') as f:
        f.write('%s\n' % ','.join(META_HEADERS))

        print '\nParsing:'
        for i in range(1, npages+1):
            get_data(i, f, assembly_id)

        print '\nMeta data written to ' + meta_data
