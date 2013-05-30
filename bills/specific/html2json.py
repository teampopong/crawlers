#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import re

import gevent
from gevent import monkey; monkey.patch_all()
import lxml
import pandas as pd

from settings import likms, DIR, X
import utils

LIKMS = likms

def extract_row_contents(row):

    def extract_subcolumn(elem):

        def urls_in_image(image):
            has_url = image.xpath('@onclick')
            url = None
            if has_url:
                matched = re.search(r'(.*)\((.*)\)', has_url[0])
                if matched.group(1)=='javascript:openConfInfo':
                    parts = re.sub('[ \']', '', matched.group(2)).split(',')
                    url = '%s/ConfInfoPopup.jsp?bill_id=%s&proc_id=%s' % (LIKMS, parts[0], parts[1])
                elif matched.group(1)=='javascript:OpenConfFile':
                    parts = re.sub(r'.*\((.*)\)', r'\g<1>',\
                            has_url[0])\
                            .replace(' ', '').replace('\'','')\
                            .split(',')
                    if parts[1] > 208:
                        url = '%sdata2/%s/pdf/%s' % (parts[0], parts[1], parts[2])
                    else:
                        url = '%sdata1/%s/%s' % (parts[0], parts[1], parts[2])
                elif matched.group(1)=='javascript:ShowProposer':
                    parts = re.sub('[ \']', '', matched.group(2))
                    url = '%s/CoactorListPopup.jsp?bill_id=%s' % (LIKMS, parts)
            return url

        texts = filter(None, (t.strip()\
                    for t in elem.xpath('descendant::text()')))

        if elem.xpath('table'):
            a_links   = [link.xpath('td/a/@href') for link in elem.xpath('descendant::tr')]
        else:
            i, node = 0, []
            elem_node = elem.xpath('descendant::node()')
            for j, n in enumerate(elem_node):
                if type(n)==lxml.etree._Element:
                    if n.tag=='br':
                        node.append(elem_node[i:j])
                        i = j
            a_links = list()
            for n in node:
                tmp = []
                for m in n:
                    if type(m)==lxml.etree._ElementUnicodeResult:
                        desc = m.strip()
                        a_links.append(tmp)
                        tmp = []

                    elif type(m)==lxml.etree._Element and m.tag not in ['img', 'br']:
                        tmp.append(m.xpath('@href')[0])
                    else:
                        pass

        img_links = [urls_in_image(img) for img in elem.xpath('descendant::img')]
        links     = a_links or img_links

        urls      = map(None, texts, links) if links else texts[0] if texts else None

        return urls

    def extract_subrows(elem_subrows):
        subrows = []
        for elem_subrow in elem_subrows:
            subrows.append(extract_subcolumn(elem_subcolumn)\
                    for elem_subcolumn in elem_subrow)
        return subrows


    titles = row.xpath('descendant::span[@class="text8" or @class="text11"]/text()')
    tables = row.xpath('descendant::table[@bgcolor="#D1D1D1"]')
    table_infos = []
    for table in tables:
        rows = table.xpath('tbody/tr')
        headers = rows[0].xpath('descendant::div/text()')
        elem_subrows = [row.xpath('descendant::td/div')  for row in rows[1:]]
        subrows = extract_subrows(elem_subrows)
        table_infos.append([dict(zip(headers, subrow)) for subrow in subrows])

    return dict(zip(titles, table_infos))


def extract_specifics(assembly_id, bill_id, meta):

    def extract_file_links(c):
        url = c.xpath('descendant::a/@href')
        i, node = 0, []
        elem_node = c.xpath('descendant::node()')
        for j, n in enumerate(elem_node):
            if type(n)==lxml.etree._Element:
                if n.tag=='br':
                    node.append(elem_node[i:j])
                    i = j
        links = dict()
        for n in node:
            tmp = []
            for m in n:
                if type(m)==lxml.etree._ElementUnicodeResult:
                    desc = m.strip()
                    links[desc] = tmp
                    tmp = []

                elif type(m)==lxml.etree._Element and m.tag not in ['img', 'br']:
                    tmp.append(m.xpath('@href')[0])
                else:
                    pass
        return links

    def extract_meeting_num(c):
        s = c.xpath('descendant::text()')[0]
        m = re.search(ur'제(.*)대.*제(.*)회', s)
        return [int(e) for e in m.groups()]

    def status_info(es, et, status_en):
        subjects = es.xpath('text()')[0]
        headers = [t[1] for t in utils.get_elem_texts(et, 'td')]

        elem_contents = [c for c in es.xpath(X['timeline']['%s_contents' % status_en]) if type(c)==lxml.etree._Element]
        elem_rows = [ec.xpath('td') for ec in elem_contents]

        rows = []
        for row in elem_rows:
            columns = []
            for column in row:
                links = column.xpath('descendant::a')
                images = column.xpath('descendant::img')
                if links:
                    columns.append([link.xpath('@href')[0] for link in links])
                elif images:
                    parts = re.sub(r'.*\((.*)\)', r'\g<1>',\
                            images[0].xpath('@onclick')[0])\
                            .replace(' ', '').replace('\'','')\
                            .split(',')
                    if parts[1] > 208:
                        url = '%sdata2/%s/pdf/%s' % (parts[0], parts[1], parts[2])
                    else:
                        url = '%sdata1/%s/%s' % (parts[0], parts[1], parts[2])
                    columns.append(url)
                else:
                    columns.append(column.xpath('descendant::text()')[1].strip())
            rows.append(dict(zip(headers, columns)))
        return rows

    fn          = '%s/%d/%s.html' % (DIR['specifics'], assembly_id, bill_id)
    page        = utils.read_webpage(fn)
    table       = utils.get_elems(page, X['spec_table'])[1]
    timeline    = page.xpath(X['spec_timeline'])[0]

    title         = page.xpath(X['spec_title'])[0].strip().replace('"','')
    status_detail = ' '.join(page.xpath(X['spec_status'])).strip()
    statuses      = filter(None,\
                    (s.strip() for s in\
                    ' '.join(\
                    s for s in timeline.xpath(X['spec_timeline_statuses'])\
                    if not type(s)==lxml.etree._Element)\
                    .split('\n')))
    status_infos  = [filter(None, i.split('*'))\
                    for i in timeline.xpath(X['spec_timeline_status_infos'])]
    row_titles = [' '.join(e.xpath('td/text()')).strip()\
            for i, e in enumerate(table.xpath('tbody/tr')) if i%4==0]
    elem_row_contents = [e.xpath('td[@class="text6"]')[0]\
            for i, e in enumerate(table.xpath('tbody/tr')) if i%4==1]
    status_dict   = {}

    for i, r in enumerate(elem_row_contents):
        if row_titles[i]!='부가정보':
            status_dict[row_titles[i]] = extract_row_contents(r)
        else:
            t = r.xpath('span[@class="text8"]/text()')
            c = filter(None, (t.strip() for t in r.xpath('text()')))
            status_dict[row_titles[i]] = dict(zip(t, c))

    headers = ['assembly_id', 'bill_id', 'title', 'status_detail', 'statuses', 'status_infos', 'status_dict']
    specifics = [assembly_id, bill_id, title, status_detail, statuses, status_infos, status_dict]

    return dict(zip(headers, specifics))

def extract_summaries(assembly_id, bill_id):
    #TODO: 제안이유 & 주요내용 분리하기
    try:
        fn = '%s/%s/%s.html' % (DIR['summaries'], assembly_id, bill_id)
        page = utils.read_webpage(fn)
        summaries = [e.strip() for e in utils.get_elems(page, X['summary'])]
        return summaries
    except IOError as e:
        return None

def extract_proposers(assembly_id, bill_id):
    #TODO: 찬성의원 목록에 의원 이름이 있는 경우가 있는자 확인
    fn = '%s/%s/%s.html' % (DIR['proposers'], assembly_id, bill_id)
    page = utils.read_webpage(fn)
    return utils.get_elems(page, X['proposers'])

def extract_withdrawers(assembly_id, bill_id):
    fn = '%s/%s/%s.html' % (DIR['withdrawers'], assembly_id, bill_id)
    page = utils.read_webpage(fn)
    return utils.get_elems(page, X['withdrawers'])

def include(meta, bill_id, attr):
    value = list(meta.ix[meta['bill_id']==str(bill_id), attr])[0]
    if pd.isnull(value):
        return None
    return value

def parse_page(assembly_id, bill_id, meta, directory):

    fn = '%s/%s.json' % (directory, bill_id)

    if not os.path.isfile(fn):
        d = extract_specifics(assembly_id, bill_id, meta)
        d['proposers']      = extract_proposers(assembly_id, bill_id)
        d['summaries']      = extract_summaries(assembly_id, bill_id)
        d['withdrawers']    = extract_withdrawers(assembly_id, bill_id)
        d['proposed_date']  = include(meta, bill_id, 'proposed_date')
        d['decision_date']  = include(meta, bill_id, 'decision_date')
        d['link_id']        = include(meta, bill_id, 'link_id')
        d['proposer_type']  = include(meta, bill_id, 'proposer_type')
        d['status']         = "계류" if include(meta, bill_id, 'status')==1 else "처리"

        utils.write_json(d, fn)

def html2json(assembly_id, range=(None, None)):
    metafile = '%s/%d.csv' % (DIR['meta'], assembly_id)
    meta = pd.read_csv(metafile, dtype={'bill_id': object, 'link_id': object})

    jsondir = '%s/%s' % (DIR['data'], assembly_id)
    utils.check_dir(jsondir)

    jobs = [gevent.spawn(parse_page, assembly_id, bill_id, meta, jsondir) for bill_id in meta['bill_id'][range[0]:range[1]]]

    gevent.joinall(jobs)
