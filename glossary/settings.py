#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

DIR = {
    'html': 'sources/html',
    'results': 'sources'
}

BASEURL = {
    'committee': 'http://committee.na.go.kr/portal/',
    # 원본 사이트는 [여기](http://likms.assembly.go.kr/bill/WebContents/Summary2.htm)인데 내용이 iframe 안에 있어서 실질적인 baseurl은 아래와 같음
    'likms': 'http://likms.assembly.go.kr/bill/WebContents/content',
    'nas': 'http://nas.na.go.kr/site?siteId=site-20111206-000001000&pageId=page-20111207-000001129&dic_mode=default&dic_pageNumber='
}

RANGE = {
    'likms': (1, 4),        # MAX: (1, 4)
    'nas': (1, 126)         # MAX: (1, 126)
}
