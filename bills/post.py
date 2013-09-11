#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
import sys
import time

from redis_queue import RedisQueue
from settings import DIR, QUEUE_NAMES, SESSION, TEMPLATE_BILL_URL
import facebook
import twitter


INTERVAL_MIN = 5
INTERVAL_SEC = INTERVAL_MIN * 60


def refine_bill_content(bill, max_field_len=30):
    # bill_id
    bill_id = bill['bill_id']

    # title
    title = bill['title']
    title = truncate(title, max_field_len)
    title_josa = ullul(title.strip('.')[-1])

    # proposer
    proposer = bill['status_dict']['접수']['의안접수정보'][0]['제안자']
    while isinstance(proposer, list):
        proposer = proposer[0]
    proposer = truncate(proposer, max_field_len)
    proposer_josa = yiga(proposer.strip('.')[-1])

    return {
        'proposer': proposer,
        'proposer_josa': proposer_josa,
        'title': title,
        'title_josa': title_josa,
        'bill_id': bill_id,
        'url': TEMPLATE_BILL_URL.format(bill_id)
    }


def post_bills_facebook(new_bills):
    if new_bills:
        print '\t'.join(new_bills)
        post_sentences = []
        post_sentences.append('오늘 국회에서 발의된 %d개의 새 의안 목록입니다.\n' % (len(new_bills)))
        for idx, bill_id in enumerate(new_bills):
            bill = get_bill(bill_id)
            bill = refine_bill_content(bill, None)
            bill['idx'] = idx
            post_sentences.append('%(idx)d. %(proposer)s, "%(title)s" %(url)s' % bill)
        post = "\n".join(post_sentences)
        facebook.post(post)


def post_bills_twitter(new_bills):
    if new_bills:
        cnt = len(new_bills)
        twitter.post('지금부터 %d분간 %d분 간격으로 %d개의 새 의안을 트윗할 예정입니다.' % (INTERVAL_MIN * cnt, INTERVAL_MIN, cnt))
    for bill_id in new_bills:
        time.sleep(INTERVAL_SEC)
        bill = get_bill(bill_id)
        post_bill_twitter(bill)
        print '%s posted' % bill['bill_id']


def post_bill_twitter(bill):
    status = '%(proposer)s%(proposer_josa)s "%(title)s"%(title_josa)s 새로 발의하였습니다. http://pokr.kr/bill/%(bill_id)s' % refine_bill_content(bill)
    twitter.post(status)


def truncate(text, max_len):
    if max_len is None:
        return text

    if len(text) > max_len:
        text = text[:max_len] + '...'
    return text


def yiga(char):
    if (ord(char) - 44032) % 28:
        return '이'
    else:
        return '가'


def ullul(char):
    if (ord(char) - 44032) % 28:
        return '을'
    else:
        return '를'


def get_bill(bill_id):
    with open('%s/%d/%s.json' % (DIR['data'], SESSION, bill_id), 'r') as f:
        bill = json.load(f)
    return bill


def usage():
    print '''post.py COMMAND

COMMAND:
    twitter
    facebook'''


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    command = sys.argv[1]
    if command == 'twitter':
        queue = RedisQueue('post_bills_twitter')
        bills = list(queue)
        post_bills_twitter(bills)
    elif command == 'facebook':
        queue = RedisQueue('post_bills_facebook')
        bills = list(queue)
        post_bills_facebook(bills)
    else:
        raise Exception('Unknown target')
