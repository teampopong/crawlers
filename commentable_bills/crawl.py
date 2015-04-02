#! /usr/bin/python
# -*- coding: utf-8 -*-

import codecs
from datetime import date
import requests
from lxml import html

# 진행중 입법예고 중 의안 크롤러 http://pal.assembly.go.kr/law/mainView.do

datadir = '.' # fill me

page = 1
targets, ids = [], ['0']

while 1:
    data = {'tmpCurrCommitteeId': '',
            'tmpCondition': 0,
            'tmpKeyword': '',
            'currCommitteeId': '',
            'searchCondition': '',
            'searchKeyword': '',
            'closedCondition': 0,
            'pageNo': page}
    r = requests.post('http://pal.assembly.go.kr/law/listView.do', data=data)
    root = html.document_fromstring(r.text)
    ids = root.xpath('//table//tr/td[1]/text()')
    if not ids[0].isdigit():
        break
    targets.extend(ids)
    page += 1

filename = '%s/%s.txt' % (datadir, date.today())
with codecs.open(filename, 'w', 'utf-8') as f:
    f.write('\n'.join(targets))
print 'Data written to %s' % filename
