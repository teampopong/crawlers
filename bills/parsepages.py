#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import re
import lxml
import pandas as pd
from settings import ASSEMBLY_ID, DIR, END_BILL, ID_MULTIPLIER, ITEMS_PER_FILE, LIST_DATA, START_PAGE, X
import utils

def extract_specifics(id, meta):

    def spec_registration(es, et):
        elem_columns = table.xpath(X['spec_entry'])
        columns = []
        for i, c in enumerate(elem_columns):
            proposer_type =\
                    list(meta.ix[meta['bill_id']==str(id), 'proposer_type'])[0]
            if i==0: # bill_id
                columns.append(c.xpath('descendant::text()')[0].strip())
            elif i==1: #proposed_date
                columns.append(c.xpath('descendant::text()')[0].strip())
            elif i==2: # proposer_representative
                rep = re.sub(ur'의원 등 [0-9]+인', '',\
                        c.xpath('descendant::text()')[0].strip())
                columns.append(rep)
            #TODO: 파일 종류 구분하기 (의안원문, 기타문서, ...)
            elif i==3: # original_bill_links
                columns.append(c.xpath('descendant::a/@href'))
            else:
                pass
        try: # assembly_id, assembly_meeting_id
            c = elem_columns[4]
            columns.extend(\
                int(e) for e\
                in re.sub(ur'제(.*)대.*제(.*)회', r'\g<1> \g<2>',\
                c.xpath('descendant::text()')[0].strip())\
                .split())
        except ValueError, e:
            c = elem_columns[5]
            columns.extend(\
                int(e) for e\
                in re.sub(ur'제(.*)대.*제(.*)회', r'\g<1> \g<2>',\
                c.xpath('descendant::text()')[0].strip())\
                .split())
        headers = [t[1] for t in utils.get_elem_texts(et, 'td')]
        return dict(zip(headers, columns))

    def spec_commission(es, et):
        elem_contents = [c for c in es.xpath(X['timeline']['commission_contents'])\
                if type(c)==lxml.etree._Element]

        subjects = es.xpath('text()')[0]
        headers = [t[1] for t in utils.get_elem_texts(et, 'td')]
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

    #TODO: nrow 받지 말고, rowname에 해당되는 row에 넣어주기
    def append_info(info, nrow, rowname, fn):
        elem_subjects = table.xpath(X['timeline']['%s_subjects' % rowname])
        elem_headers = table.xpath(X['timeline']['%s_headers' % rowname])
        descs = []
        for i, ez in enumerate(zip(elem_subjects, elem_headers)):
            #descs.append(spec_registration(ez[0], ez[1]))
            descs.append(fn(ez[0], ez[1]))
        subjects = [e.xpath('text()')[0] for e in elem_subjects]
        info[nrow] = dict(zip(subjects, descs))


    fn = '%s/%d.html' % (DIR['specifics'], id)
    page = utils.read_webpage(fn)
    table = utils.get_elems(page, X['spec_table'])[1]

    # title, status_detail
    title = page.xpath(X['spec_title'])[0].strip()
    status_detail = ' '.join(page.xpath(X['spec_status'])).strip()

    # status_timeline
    tl = page.xpath(X['spec_timeline'])[0]
    stages = filter(None,\
            (s.strip() for s in\
                ' '.join(\
                s for s in tl.xpath(X['spec_timeline_stages'])\
                if not type(s)==lxml.etree._Element)\
                .split('\n')))
    info = [filter(None, i.split('*'))\
            for i in tl.xpath(X['spec_timeline_info'])]
    append_info(info, 0, 'registration', spec_registration)
    append_info(info, 1, 'commission', spec_commission)
    status_timeline = map(None, stages, info)

    headers = ['title', 'status_detail', 'status_timeline']
    specifics = [title, status_detail, status_timeline]

    return zip(headers, specifics)

def extract_summaries(id):
    #TODO: 제안이유 & 주요내용 분리하기
    fn = '%s/%d.html' % (DIR['summaries'], id)
    try:
        page = utils.read_webpage(fn)
        summaries = [e.strip() for e in utils.get_elems(page, X['summary'])]
    except IOError, e:
        summaries = []
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
    summaries = extract_summaries(id)
    proposers = extract_proposers(id)
    withdrawers = extract_withdrawers(id)

    #headers = ['title', 'status_detail', 'status_timeline', 'bill_id', 'proposed_date', 'proposer_representative', 'original_bill_links', 'assembly_id', 'assembly_meeting_id']
    d = dict(specifics)
    d['summaries']      = summaries
    d['proposers']      = proposers
    d['withdrawers']    = withdrawers
    d['decision_date']  = include(meta, id, 'decision_date')
    d['has_summaries']  = include(meta, id, 'has_summaries')
    d['link_id']        = include(meta, id, 'link_id')
    d['proposer_type']  = include(meta, id, 'proposer_type')
    d['status']         = include(meta, id, 'status')
    return d

if __name__=='__main__':

    meta = pd.read_csv(LIST_DATA)

    directory = '%s/%d' % (DIR['data'], ASSEMBLY_ID)
    utils.check_dir(directory)
    #TODO: ZZ로 시작하는 의안들을 위해 glob 사용

    '''
    for i in range(START_PAGE, END_BILL/ITEMS_PER_FILE + 1):
        print '\npage %d' % i
        tmp = []
        for j in range(ITEMS_PER_FILE):
            idx = ((i - 1) * ITEMS_PER_FILE) + j + 1
            if idx <= END_BILL:
                num = (ASSEMBLY_ID * ID_MULTIPLIER) + idx
                tmp.append(extract_all(num, meta))
                print num
        utils.write_json(tmp, '%s/%d.json' % (directory, i))
    '''

    d = extract_all(1900335, meta)
    utils.write_json(d, 'sample.json')
