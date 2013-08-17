#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import specific
from shutil import copyfile
import pdf
import re

from redis_queue import RedisQueue
from settings import BASEURL, DIR, PAGE_SIZE, REDIS_SETTINGS, SESSION, X
import utils


bill_s, bill_e = None, None


def get_new(a):
    print '## Get meta data'
    new_bill_ids = fetch_new_bill_ids(a)

    queue = RedisQueue('new_bill_ids')
    for bill_id in new_bill_ids:
        queue.put(bill_id)

    print '## Get specific data'
    specific.get_html(a, bill_ids=new_bill_ids)
    specific.html2json(a, bill_ids=new_bill_ids)

    print '## Get pdfs'
    pdf.get_pdf(a, bill_ids=new_bill_ids)


def update(a):
    print '## Get specific data'
    specific.get_html(a, range=(bill_s, bill_e))
    specific.html2json(a, range=(bill_s, bill_e))

    print '## Get pdfs'
    pdf.get_pdf(a, range=(bill_s, bill_e))


def fetch_new_bill_ids(assembly_id):
    directory = DIR['meta']
    meta_data = '%s/%d.csv' % (directory, assembly_id)

    lines = list(open(meta_data, 'r'))[1:]
    lines = [line.decode('utf-8') for line in lines]
    existing_ids = set(line.split(',', 1)[0].strip('"') for line in lines)
    last_proposed_date = max(line.split('","', 6)[5].strip('"') for line in lines)
    baseurl = BASEURL['list']
    url = '%(baseurl)sPROPOSE_FROM=%(last_proposed_date)s&PAGE_SIZE=100' % locals()

    directory = '%s/%s' % (DIR['list'], assembly_id)
    fn = '%s/tmp.html' % directory

    utils.get_webpage(url, fn)
    p = utils.read_webpage(fn)
    rows = utils.get_elems(p, X['table'])

    new_bill_ids = []
    with open(meta_data, 'a') as f:
        for r in reversed(rows):
            columns = r.xpath(X['columns'])
            if len(columns)==8:
                p = parse_columns(columns)
                if p[0] not in existing_ids:
                    list_to_file(p, f)
                    new_bill_ids.append(p[0])
    return new_bill_ids


def list_to_file(l, f):
    f.write('"')
    f.write('","'.join(l).encode('utf-8'))
    f.write('"\n')


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


def parse_columns(columns):
    data = []
    for j, c in enumerate(columns):
        if j==1:
            status = str(int(\
                   re.findall(r'[0-9]+', c.xpath('img/@src')[0])[0]))
            title = c.xpath('a/text()')[0].replace('"','\'')
            link = re.findall(r'\w+', c.xpath('a/@href')[0])[2]
            data.extend([status, title, link])
        elif j==6:
            data.append('1' if c.xpath('img/@onclick') else '0')
        else:
            data.append(c.xpath('text()')[0].strip())
    return data


def main(cmd):
    if cmd == 'new':
        get_new(SESSION)
    elif cmd == 'update':
        update(SESSION)
    else:
        raise Exception('invalid command')


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
