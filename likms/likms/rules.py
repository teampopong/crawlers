__all__ = ['likms_url', 'XPATHS']

BASE_URL = 'http://likms.assembly.go.kr/bill/jsp'

URL_FMTS = {
    'new-bill-list': '{BASE_URL}/BillSearchResult.jsp'
                     '?PROPOSE_FROM={date_since}&PAGE_SIZE={size}'
}

XPATHS = {
    'new-bill-list': '//table[@width="970"]'
                     '//table[@width="100%"]'
                     '//table[@width="100%"]'
                     '//tr[not(@bgcolor="#DBDBDB")][position()>1]',
    'columns': 'descendant::td',
}

def likms_url(target, **kwargs):
    return URL_FMTS[target].format(BASE_URL=BASE_URL, **kwargs)

