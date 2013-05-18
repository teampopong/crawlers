#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import lxml
import pandas as pd

from settings import ASSEMBLY_ID, DIR, END_BILL, ID_MULTIPLIER, LIST_DATA, START_BILL, X
import utils

TERMS = utils.read_terms()

def extract_specifics(id, meta):

    def registration_info(es, et, status_en):

        def extract_bill_id(c):
            return c.xpath('descendant::text()')[0].strip()
        def extract_proposed_date(c):
            return c.xpath('descendant::text()')[0].strip()
        def extract_proposer_representative(c):
            return re.sub(ur'의원 등 [0-9]+인', '',\
                    c.xpath('descendant::text()')[0].strip())
        def extract_original_bill_links(c):
            return c.xpath('descendant::a/@href')
        def extract_meeting_num(c):
            s = c.xpath('descendant::text()')[0]
            m = re.search(ur'제(.*)대.*제(.*)회', s)
            return [int(e) for e in m.groups()]

        headers = [t[1] for t in utils.get_elem_texts(et, 'td')]
        columns = [None] * len(headers)

        elem_columns = table.xpath(X['spec_entry'])
        columns[0] = extract_bill_id(elem_columns[0])
        columns[1] = extract_proposed_date(elem_columns[1])
        columns[2] = extract_proposer_representative(elem_columns[2])
        #TODO: 파일 종류 구분하기 (의안원문, 기타문서, ...)
        columns[3] = extract_original_bill_links(elem_columns[3])
        if len(headers)==6:
            try:
                columns[4] = extract_summaries(id)
            except IOError as e:
                pass
            try:
                columns[5] = extract_meeting_num(elem_columns[5])
            except (AttributeError, IndexError) as e:
                columns[5] = extract_meeting_num(elem_columns[4])
        else:
            columns[4] = extract_meeting_num(elem_columns[4])

        return dict(zip(headers, columns))

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

    def append_status(status_dict, status, fn):
        status_en = TERMS[status]
        elem_subjects = table.xpath(X['timeline']['%s_subjects' % status_en])
        elem_headers = table.xpath(X['timeline']['%s_headers' % status_en])
        descs = []
        for i, ez in enumerate(zip(elem_subjects, elem_headers)):
            descs.append(fn(ez[0], ez[1], status_en))
        subjects = [e.xpath('text()')[0] for e in elem_subjects]
        if status_dict[status]:
            status_dict[status] = dict(zip(subjects, descs))


    fn = '%s/%d.html' % (DIR['specifics'], id)
    page = utils.read_webpage(fn)
    table = utils.get_elems(page, X['spec_table'])[1]

    # title, status_detail
    title = page.xpath(X['spec_title'])[0].strip()
    status_detail = ' '.join(page.xpath(X['spec_status'])).strip()

    # statuses, status_infos, status_timeline
    tl = page.xpath(X['spec_timeline'])[0]
    statuses = filter(None,\
            (s.strip() for s in\
                ' '.join(\
                s for s in tl.xpath(X['spec_timeline_statuses'])\
                if not type(s)==lxml.etree._Element)\
                .split('\n')))
    status_infos = [filter(None, i.split('*'))\
            for i in tl.xpath(X['spec_timeline_status_infos'])]
    #status_timeline= map(None, statuses, status_infos)

    # status_dict
    status_dict = dict(map(None, statuses, status_infos))
    for status in statuses:
        fn = registration_info if status=='접수' else status_info
        try:
            append_status(status_dict, status, fn)
        except KeyError, e:
            pass

    headers = ['title', 'status_detail', 'statuses', 'status_infos', 'status_dict']
    specifics = [title, status_detail, statuses, status_infos, status_dict]

    return zip(headers, specifics)

def extract_summaries(id):
    #TODO: 제안이유 & 주요내용 분리하기
    fn = '%s/%d.html' % (DIR['summaries'], id)
    page = utils.read_webpage(fn)
    summaries = [e.strip() for e in utils.get_elems(page, X['summary'])]
    return summaries

def extract_proposers(id):
    #TODO: 찬성의원 목록에 의원 이름이 있는 경우가 있는자 확인
    fn = '%s/%d.html' % (DIR['proposers'], id)
    page = utils.read_webpage(fn)
    return utils.get_elems(page, X['proposers'])

def extract_withdrawers(id):
    fn = '%s/%d.html' % (DIR['withdrawers'], id)
    page = utils.read_webpage(fn)
    return utils.get_elems(page, X['withdrawers'])

def include(meta, id, attr):
    value = list(meta.ix[meta['bill_id']==str(id), attr])[0]
    if pd.isnull(value):
        return None
    return value

def extract_all(id, meta):
    specifics = extract_specifics(id, meta)
    proposers = extract_proposers(id)
    withdrawers = extract_withdrawers(id)

    d = dict(specifics)
    d['proposers']      = proposers
    d['withdrawers']    = withdrawers
    d['decision_date']  = include(meta, id, 'decision_date')
    d['link_id']        = include(meta, id, 'link_id')
    d['proposer_type']  = include(meta, id, 'proposer_type')
    d['status']         = "계류" if include(meta, id, 'status')==1 else "처리"
    return d

if __name__=='__main__':

    meta = pd.read_csv(LIST_DATA)

    directory = '%s/%d' % (DIR['data'], ASSEMBLY_ID)
    utils.check_dir(directory)

    #TODO: ZZ로 시작하는 의안들을 위해 glob 사용
    for i in range(START_BILL, END_BILL+1):
        num = (ASSEMBLY_ID * ID_MULTIPLIER) + i
        d = extract_all(num, meta)
        utils.write_json(d, '%s/%d.json' % (directory, num))
