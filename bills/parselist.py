#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import re

import lxml
import utils
from settings import NUM_PAGES, END_BILL, DIR, META_DATA, BASEURL, X

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
            if url:
                d = '1'
            else:
                d = '0'
            data.append(d)
        else:
            data.append(c.xpath('text()')[0].strip())
    return data

def get_data(i, f):
    fn = '%s/%s.html' % (DIR['list'], i)
    page = utils.read_webpage(fn)
    rows = utils.get_elems(page, X['table'])

    for r in rows:
        columns = r.xpath(X['columns'])
        if len(columns)==8:
            f.write('"')
            f.write('","'.join(extract(columns)).encode('utf-8'))
            f.write('"\n')
    print fn

if __name__=='__main__':
    utils.check_dir(DIR['meta'])
    with open(META_DATA, 'wa') as f:
        f.write('"bill_id","status","title","link_id","proposer_type","proposed_date","decision_date","decision_result","has_summaries","status_detail"\n')
        for i in range(END_BILL/NUM_PAGES+3):
            get_data(i+1, f)
        print 'Meta data written to ' + META_DATA
