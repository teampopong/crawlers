#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import meta
import specific
import pdf
import re

import utils
from settings import BASEURL, DIR, PAGE_SIZE, X


bill_s, bill_e = None, None


def get(a):
    print '## Get meta data'
    append_new_bills(a)

    print '## Get specific data'
    specific.get_html(a, range=(bill_s, bill_e))
    bills_in_progress = specific.html2json(a, range=(bill_s, bill_e))

    print '## Get pdfs'
    pdf.get_pdf(a, range=(bill_s, bill_e))

    rewrite_meta(a, bills_in_progress)

def append_new_bills(assembly_id):
    directory = DIR['meta']
    meta_data = '%s/%d.csv' % (directory, assembly_id)

    lines = list(open(meta_data, 'r'))[1:]
    existing_ids = set(line.split(',', 1)[0].strip('"') for line in lines)
    last_proposed_date = max(line.split(',', 6)[5].strip('"') for line in lines)
    baseurl = BASEURL['list']
    url = '%(baseurl)sPROPOSE_FROM=%(last_proposed_date)s&PROPOSE_TO=%(last_proposed_date)s&PAGE_SIZE=100' % locals()

    directory = '%s/%s' % (DIR['list'], assembly_id)
    fn = '%s/tmp.html' % directory

    utils.get_webpage(url, fn)
    p = utils.read_webpage(fn)
    rows = utils.get_elems(p, X['table'])

    with open(meta_data, 'a') as f:
        for r in reversed(rows):
            columns = r.xpath(X['columns'])
            if len(columns)==8:
                p = parse_columns(columns)
                if p[0] not in existing_ids:
                    list_to_file(p, f)


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


def rewrite_meta(assembly_id, bills_in_progress):
    print bills_in_progress
    bills_in_progress = set(bills_in_progress)
    to_remain = []

    directory = DIR['meta']
    meta_data = '%s/%d.csv' % (directory, assembly_id)

    for line in open(meta_data, 'r'):
        bill_id = line.split(',', 1)[0].strip('"')
        if bill_id in bills_in_progress:
            to_remain.append(line)

    with open(meta_data, 'w') as f:
        for line in to_remain:
            f.write(line)


if __name__ == '__main__':
    get(19)
