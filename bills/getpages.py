#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import pandas as pd

from settings import ASSEMBLY_ID, BASEURL, DIR, END_BILL, ID_MULTIPLIER, LIST_DATA
import utils

def get_urlmap():
    with open(LIST_DATA, 'r') as f:
        data = pd.read_csv(f)
    return zip(data['bill_id'], data['link_id'], data['has_summaries'])

def get_pages(bill_id, link_id, has_summaries):
    #TODO: 파일들이 다 있는지 확인하고, if not, 재다운로드 시도
    #TODO: ZZ 파일들은 한 번 더 시도
    def get_specifics():
        outp = '%s/%s.html' % (DIR['specifics'], bill_id)
        utils.get_webpage(BASEURL['specific'] + link_id, outp)
    def get_summaries():
        if has_summaries==1:
            outp = '%s/%s.html' % (DIR['summaries'], bill_id)
            utils.get_webpage(BASEURL['summary'] + link_id, outp)
    def get_proposers():
        outp = '%s/%s.html' % (DIR['proposers'], bill_id)
        utils.get_webpage(BASEURL['proposer_list'] + link_id, outp)
    def get_withdrawers():
        outp = '%s/%s.html' % (DIR['withdrawers'], bill_id)
        utils.get_webpage(BASEURL['withdrawers'] + link_id, outp)

    get_specifics()
    get_summaries()
    get_proposers()
    get_withdrawers()

def check_missing(typename, nbills):
    a = ASSEMBLY_ID * ID_MULTIPLIER
    A = [str(a + b + 1) for b in range(nbills)]
    B = [f.strip('.html') for f in os.listdir(DIR[typename])]
    return [c for c in A if c not in B]

if __name__=='__main__':

    utils.check_dir(DIR['summaries'])
    utils.check_dir(DIR['specifics'])
    utils.check_dir(DIR['proposers'])
    utils.check_dir(DIR['withdrawers'])

    urlmap = get_urlmap()

    #TODO: get urlmap range input from settings
    for bill_id, link_id, has_summaries in urlmap:
        get_pages(bill_id, link_id, has_summaries)
        print bill_id

    missing = check_missing('specifics', END_BILL)
    print missing

    #TODO: donot input link_id, has_summaries
    #get_pages('1901020', 'PRC_C1G2G0V8D0B2H1S5I4J2Z4G9N2B0F6', 1)
