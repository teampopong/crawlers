#! /usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function

from . import settings as s
from . import utils


BASEURL = 'http://likms.assembly.go.kr/bill/jsp/LatestReceiptBill.jsp'
DATA = {
    'ORDER_COLUMN': 'ProposeDt Desc, BillNo',
    'ORDER_TYPE': 'DESC',
    'PAGE_SIZE': 100,
    'ALL_COUNT': 1470,
    'RESULT_COUNT': 10,
    'PAGE': 1,
}
XPATH = '//table[2]/tbody/tr[3]/td[1]/table/tbody/tr[2]/td[2]/table/tbody/tr[not(@bgcolor)]'


@utils.catch
def parse_row(row):
    def row_xpath(row, xpath):
        return ','.join(row.xpath(xpath))

    return {
        'id': row_xpath(row, './td[1]/text()'),
        'likms_id': row_xpath(row, './td[2]/a/@href').split("'")[1],
        'title': row_xpath(row, './td[2]/a/text()'),
        'proposer': row_xpath(row, './td[3]/text()'),
        'proposed_date': row_xpath(row, './td[4]/text()'),
        'created_at': utils.now(),
        'committee': row_xpath(row, './td[5]/@title')
    }


def page(pagenum, db):
    DATA['PAGE'] = pagenum
    root = utils.get_root(BASEURL, DATA, method='POST')
    rows = root.xpath(XPATH)
    page = list(filter(None, [parse_row(row) for row in rows[1:-2]]))

    for row in page:
        id_ = row['id']
        if db['bill_list'].find_one({'id': id_}):
            print('Found duplicate %s at page %s' % (id_, pagenum), end='\t')
            return (page, True)
        else:
            db['bill_list'].insert_one(row)

    return (page, False)


def pages(collection='bill_list', maxpage=100):
    print(utils.now(), end='\t')
    db = utils.init_db(s.MONGODB_URI, s.MONGODB_NAME)
    count = db[collection].count()

    pagenum = 1
    terminate = False
    while terminate==False or pagenum > maxpage:
        rows, terminate = page(pagenum, db)
        pagenum += 1

    added = db[collection].count() - count
    print('Added %s, now %s records' % (added, count))


if __name__=='__main__':
    pages()
