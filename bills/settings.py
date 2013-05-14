#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

NUM_PAGES = 50
MAX_PAGE = 65535
LIST_DIR = 'list'
LIST_DATA = 'list.csv'
BASEURL = {
    'list': 'http://likms.assembly.go.kr/bill/jsp/BillSearchResult.jsp?AGE_FROM=19&AGE_TO=19&',
    'summary': 'http://likms.assembly.go.kr/bill/jsp/SummaryPopup.jsp?bill_id=',
    'specific': 'http://likms.assembly.go.kr/bill/jsp/BillDetail.jsp?bill_id='
}
X = {
    'table'  : '//table[@width="970"]//table[@width="100%"]//table[@width="100%"]//tr[not(@bgcolor="#DBDBDB")][position()>1]',
    'columns': 'descendant::td',
}

