#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import re
import lxml
import pandas as pd
from settings import ASSEMBLY_ID, DIR, END_BILL, ID_MULTIPLIER, ITEMS_PER_FILE, LIST_DATA, START_PAGE, X
import utils

def extract_specifics(id, meta):
    fn = '%s/%d.html' % (DIR['specifics'], id)
    #TODO: 다른 항목들 가져오기 (위원회 심사, 부가정보, 등)
    page = utils.read_webpage(fn)
    table = utils.get_elems(page, X['spec_table'])[1]

    # title, status_detail
    title = page.xpath(X['spec_title'])[0].strip()
    status_detail = ' '.join(page.xpath(X['spec_status'])).strip()
    specifics = [title, status_detail]

    # status_timeline
    tl = page.xpath(X['spec_timeline'])[0]
    stages = (s.strip() for s in\
                ' '.join(\
                s for s in tl.xpath(X['spec_timeline_stages'])\
                if not type(s)==lxml.etree._Element)\
                .split('\n'))
    info = (filter(None, i.split('*'))\
            for i in tl.xpath(X['spec_timeline_info']))
    specifics.append(map(None, stages, info))

    columns = table.xpath(X['spec_entry'])
    for i, c in enumerate(columns):
        proposer_type =\
                list(meta.ix[meta['bill_id']==str(id), 'proposer_type'])[0]

        # bill_id
        if i==0:
            specifics.append(c.xpath('descendant::text()')[0].strip())

        #proposed_date
        elif i==1:
            specifics.append(c.xpath('descendant::text()')[0].strip())

        # proposer_representative
        elif i==2:
            rep = re.sub(ur'의원 등 [0-9]+인', '',\
                    c.xpath('descendant::text()')[0].strip())
            specifics.append(rep)

        # original_bill_links
        #TODO: 파일 종류 구분하기 (의안원문, 기타문서, ...)
        elif i==3:
            specifics.append(c.xpath('descendant::a/@href'))

        else:
            pass

    # assembly_id, assembly_meeting_id
    try:
        c = columns[4]
        specifics.extend(\
            int(e) for e\
            in re.sub(ur'제(.*)대.*제(.*)회', r'\g<1> \g<2>',\
            c.xpath('descendant::text()')[0].strip())\
            .split())
    except ValueError, e:
        c = columns[5]
        specifics.extend(\
            int(e) for e\
            in re.sub(ur'제(.*)대.*제(.*)회', r'\g<1> \g<2>',\
            c.xpath('descendant::text()')[0].strip())\
            .split())

    return specifics

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

    headers = ['title', 'status_detail', 'status_timeline', 'bill_id', 'proposed_date', 'proposer_representative', 'original_bill_links', 'assembly_id', 'assembly_meeting_id']
    d = dict(zip(headers, specifics))
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

    d = extract_all(1900332, meta)
    utils.write_json(d, 'sample.json')
