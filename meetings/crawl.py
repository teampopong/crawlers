#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import json
import os
import re
import urllib

import get

basedir = '.'   # change me
jsondir = '%s/meetings' % basedir
pdfdir = '%s/meeting-docs' % basedir

baseurl = 'http://likms.assembly.go.kr/record'

def checkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_html(page_num):
    url = '%s/new/new_list.jsp?CLASS_CODE=0&currentPage=%d' % (baseurl, page_num)
    r = get.htmltree(url)
    return r.read().decode('euc-kr').encode('utf-8')

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

def get_filename(data, filetype):
    if filetype=='json':
        directory = jsondir
    elif filetype=='pdf':
        directory = pdfdir
    a, s, m = data['assembly_id'], data['session_id'], data['meeting_id']
    c, d = data['committee'], data['date']
    checkdir('%s/%s/%s' % (directory, a, d))
    filename = '%s/%s/%s/%s-%s-%s-%s.%s'\
            % (directory, a, d, a, s, m, c, filetype)
    return filename

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
                try:
                    v = get.text(v, '.')[0]
                    if v.startswith(u'제'):
                        row[k] = re.search('[0-9]+', v).group(0)
                except AttributeError:
                    pass

    def parse_others(row):
        del row['n']
        for k, v in row.items():
            flag = isinstance(v, str) or isinstance(v, unicode)\
                    or isinstance(v, list)
            if not flag:
                row[k] = get.text(v, '.')[0]

    def check_elems(attrs, elems):
        if len(elems)!=len(attrs):
            check = [e.xpath('./@colspan') for e in elems]
            for c in check:
                if c:
                    idx = int(c[0]) + 1
                    elems = elems[:idx] + ['']*(idx-2) + elems[idx:]
        return elems

    elems = check_elems(attrs, row.xpath('.//td'))
    row = dict(zip(attrs, elems))
    parse_committee(row)
    parse_date(row)
    parse_issues(row)
    parse_ids(row)
    parse_others(row)
    return row

def parse_page(page_num, attrs):

    def save_pdf(data):
        filename = get_filename(data, 'pdf')
        urllib.urlretrieve(data['pdf'], filename)

    def save_json(data):
        filename = get_filename(data, 'json')
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    html = get_html(page_num)
    root = get.webpage(html)
    rows = root.xpath(\
            '//table[@background="../img/main_boxback2.gif"]//tr')[2:-1]
    for row in rows:
        data = parse_row(row, attrs)
        save_json(data)
        save_pdf(data)

if __name__=='__main__':
    attrs = ['n', 'assembly_id', 'session_id', 'meeting_id', 'committee',\
            'issues', 'date']
    for page_num in range(1, 4):
        print page_num; parse_page(page_num, attrs)
