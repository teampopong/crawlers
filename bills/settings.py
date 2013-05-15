#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

likms = 'http://likms.assembly.go.kr/bill/jsp'

NUM_PAGES = 50
MAX_PAGE = 4961
LIST_DATA = 'na-bills-19.csv'

DIR = {
    'list'         : 'html/list',
    'summaries'    : 'html/summaries',
    'specifics'    : 'html/specifics',
    'proposers'    : 'html/proposers',
    'withdrawers'  : 'html/withdrawers'
}
BASEURL = {
    'list'         : likms + '/BillSearchResult.jsp?AGE_FROM=19&AGE_TO=19&',
    'summary'      : likms + '/SummaryPopup.jsp?bill_id=',
    'specific'     : likms + '/BillDetail.jsp?bill_id=',
    'proposer_list': likms + '/CoactorListPopup.jsp?bill_id=',
    'withdrawers'  : likms + '/ReturnListPopup.jsp?bill_id='
}
X = {
    'columns'      : 'descendant::td',
    'spec_table'   : '//table[@width="940"]',
    'spec_entry'   : 'descendant::tr[@bgcolor="#EAF2ED"]/following-sibling::tr/td/div',
    'spec_status'  : '//td[@background="/bill/WebContents/BillDetail/circle_11.gif"]/text()',
    'spec_timeline': '//td[@bgcolor="#FEFFEF" and not(@id="SUMMARY_CONTENTS")]/table//tr',
    'spec_title'   : '//td[@height="33" and @class="title_large"]/text()',
    'summary'      : '//span[@class="text6_1"]/text()',
    'proposers'    : '//td[@width="10%" and @height="20"]/text()',
    'table'        : '//table[@width="970"]//table[@width="100%"]//table[@width="100%"]//tr[not(@bgcolor="#DBDBDB")][position()>1]'
}
