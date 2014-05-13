#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import json
import re

import get

baseurl = 'http://likms.assembly.go.kr/record'

def download(page):
    url = '%s/new/new_list.jsp?CLASS_CODE=0&currentPage=%d' % (baseurl, page)
    with open ('html/%d.html' % page, 'w') as f:
        r = get.htmltree(url)
        f.write(r.read().decode('euc-kr').encode('utf-8'))

def get_hidden_url(url):
    f = get.htmltree(url.encode('utf-8'))
    root = get.webpage(f)
    return '%s/%s' % (baseurl, root.xpath('//frame/@src')[1])

def get_issues(url):
    f = get.htmltree(url)
    if 'new_list2.jsp' in url:
        elems = get.webpage(f).xpath('//a/text()')
    elif 'new_list3.jsp' in url:
        elems = get.webpage(f).xpath('//td/@title')
    else:
        raise Exception('New DOM type.')
    return elems

def parse_row(row, attrs):
    def parse_committee(row):
        if 'committee' not in row: return
        c = row['committee']
        row['pdf'] = c.xpath('.//@onclick')[0].split("'")[1]
        row['committee'] = ' '.join(get.text(c, '.'))

    def parse_date(row):
        if 'date' not in row: return
        row['date'] = get.text(row['date'], '.')[0].replace('.', '-')

    def parse_issues(row):
        if 'issues' not in row: return
        part_url = row['issues'].xpath('.//@onclick')[0].split("'")[1][3:]
        issues_url = '%s/%s' % (baseurl, part_url)
        row['issues_url'] = get_hidden_url(issues_url)
        row['issues'] = get_issues(row['issues_url'])

    def parse_ids(row):
        for k, v in row.items():
            if k.endswith('_id'):
                row[k] = re.search('[0-9]+', get.text(v, '.')[0]).group(0)

    def parse_others(row):
        del row['n']
        for k, v in row.items():
            flag = isinstance(v, str) or isinstance(v, unicode)\
                    or isinstance(v, list)
            if not flag:
                row[k] = get.text(v, '.')[0]

    row = dict(zip(attrs, row))
    parse_committee(row)
    parse_date(row)
    parse_issues(row)
    parse_ids(row)
    parse_others(row)
    return row

def parse_page(page, attrs):
    nattrs = len(attrs)
    rows = [page[i*nattrs:(i+1)*nattrs] for i in range(len(page)/nattrs)][1:]
    for row in rows:
        data = parse_row(row, attrs)
        a, s, m = data['assembly_id'], data['session_id'], data['meeting_id']
        c, d = data['committee'], data['date']
        with open('json/%s-%s-%s-%s-%s.json' % (d, a, s, m, c), 'w') as f:
            json.dump(data, f)

def page2json(page, attrs):
    print page
    with open('html/%d.html' % page, 'r') as f:
        html = f.read()
    root = get.webpage(html)
    page = root.xpath('//table[@background="../img/main_boxback2.gif"]//td')[1:-1]
    parse_page(page, attrs)

if __name__=='__main__':
    attrs = ['n', 'assembly_id', 'session_id', 'meeting_id', 'committee',\
            'issues', 'date']
    for page in range(1, 64):
        page2json(page, attrs)
