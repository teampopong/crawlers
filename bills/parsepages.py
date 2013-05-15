#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import re
import math
import pandas as pd
from settings import DIR, X, LIST_DATA
import utils

#TODO: committee은 어디에 있는지 찾기
def extract_specifics(fn):
    #TODO: 다른 항목들 가져오기 (위원회 심사, 부가정보)
    page = utils.read_webpage(fn)
    table = utils.get_elems(page, X['spec_table'])[1]

    # title, status_detail
    title = page.xpath(X['spec_title'])[0].strip()
    status_detail = ' '.join(page.xpath(X['spec_status'])).strip()
    specifics = [title, status_detail]

    #TODO: status_timeline
    #timeline = page.xpath(X['spec_timeline'])[0]
    #print timeline

    for i, c in enumerate(table.xpath(X['spec_entry'])):
        # bill_id
        if i==0:
            #TODO: proposer representative에서 이름만 남기기
            specifics.append(int(c.xpath('descendant::text()')[0].strip()))
        #proposed_date
        elif i==1:
            specifics.append(c.xpath('descendant::text()')[0].strip())
        # proposer_representative
        elif i==2:
            rep = re.sub(ur'의원 등 [0-9]+인', '',\
                    c.xpath('descendant::text()')[0].strip())
            specifics.append(rep)
        # original_bill_links
        elif i==3:
            specifics.append(c.xpath('descendant::a/@href'))
        # assembly_id, assembly_meeting_id
        elif i==5:
            specifics.extend(\
                    int(e) for e\
                    in re.sub(ur'제(.*)대.*제(.*)회', r'\g<1> \g<2>',\
                    c.xpath('descendant::text()')[0].strip())\
                    .split())
        else:
            pass
    return specifics

def extract_summaries(fn):
    #TODO: 제안이유 & 주요내용 분리하기
    try:
        page = utils.read_webpage(fn)
        summaries = [e.strip() for e in utils.get_elems(page, X['summary'])]
    except AttributeError, e:
        summaries = []
    return summaries

def extract_proposers(fn):
    #TODO: 찬성의원 목록에 의원 이름이 있는 경우가 있는자 확인
    page = utils.read_webpage(fn)
    return utils.get_elems(page, X['proposers'])

def extract_withdrawers(fn):
    #TODO: http://likms.assembly.go.kr/bill/jsp/ReturnListPopup.jsp?bill_id=
    return fn

def include(meta, i, attr, _type='str'):
    value = list(meta.ix[meta['bill_id']==str(i), attr])[0]
    if _type=='float':
        if math.isnan(value):
            return None
    else:
        pass
    return value

if __name__=='__main__':

    meta = pd.read_csv(LIST_DATA)

    i = 1900003
    specifics = extract_specifics('%s/%d.html' % (DIR['specifics'], i))
    summaries = extract_summaries('%s/%d.html' % (DIR['summaries'], i))
    proposers = extract_proposers('%s/%d.html' % (DIR['proposers'], i))
    withdrawers = extract_withdrawers('%s/%d.html' % (DIR['withdrawers'], i))

    headers = ['title', 'status_detail', 'bill_id', 'proposed_date', 'proposer_representative', 'original_bill_links', 'assembly_id', 'assembly_meeting_id']
    d = dict(zip(headers, specifics))
    d['summaries']      = summaries
    d['proposers']      = proposers
    d['decision_date']  = include(meta, i, 'decision_date', 'float')
    d['decision_result']= include(meta, i, 'decision_result', 'float')
    d['has_summaries']  = include(meta, i, 'has_summaries')
    d['link_id']        = include(meta, i, 'link_id')
    d['proposer_type']  = include(meta, i, 'proposer_type')
    d['status']         = include(meta, i, 'status', 'float')

    utils.write_json(d, 'sample.json')
