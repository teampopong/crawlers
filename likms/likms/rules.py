from settings import DATA_DIR


__all__ = ['filepath', 'likms_url', 'XPATHS']

BASE_URL = 'http://likms.assembly.go.kr/bill/jsp'

URL_FMTS = {
    'new-bill-list': '{BASE_URL}/BillSearchResult.jsp'
                      '?PROPOSE_FROM={date_since}&PAGE_SIZE={size}',
    'bill-spec': '{BASE_URL}/BillDetail.jsp?bill_id={link_id}',
    'bill-summary': '{BASE_URL}/SummaryPopup.jsp?bill_id={link_id}',
    'bill-proposers': '{BASE_URL}/CoactorListPopup.jsp?bill_id={link_id}',
    'bill-withdrawers': '{BASE_URL}/ReturnListPopup.jsp?bill_id={link_id}',
}

XPATHS = {
    'new-bill-list': '//table[@width="970"]'
                     '//table[@width="100%"]'
                     '//table[@width="100%"]'
                     '//tr[not(@bgcolor="#DBDBDB")][position()>1]',
    'columns': 'descendant::td',
}

FILEPATH_FMTS = {
    'bill-spec-html': '{DATA_DIR}/sources/specifics/{assembly_id}/{bill_id}.html',
    'bill-summary-html': '{DATA_DIR}/sources/summaries/{assembly_id}/{bill_id}.html',
    'bill-proposers-html': '{DATA_DIR}/sources/proposers/{assembly_id}/{bill_id}.html',
    'bill-withdrawers-html': '{DATA_DIR}/sources/withdrawers/{assembly_id}/{bill_id}.html'
}


def likms_url(target, **kwargs):
    return URL_FMTS[target].format(BASE_URL=BASE_URL, **kwargs)

def filepath(target, **kwargs):
    return FILEPATH_FMTS[target].format(DATA_DIR=DATA_DIR, **kwargs)

