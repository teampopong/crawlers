#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import pandas as pd

from settings import ASSEMBLY_ID, BASEURL, DIR, END_BILL, ID_MULTIPLIER, META_DATA
import utils

def get_metadata():
    meta = {}
    with open(META_DATA, 'r') as f:
        data = pd.read_csv(f)
    for d in zip(data['bill_id'], data['link_id'], data['has_summaries']):
        meta[d[0]] = (d[1], d[2])
    return meta

def get_pages(bill_id, metadata):
    link_id, has_summaries = metadata[bill_id]

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
    #TODO: 파일들이 다 있는지 확인하고, if not, 재다운로드 시도 (ZZ 파일들 감안)
    a = ASSEMBLY_ID * ID_MULTIPLIER
    A = [str(a + b + 1) for b in range(nbills)]
    B = [f.strip('.html') for f in os.listdir(DIR[typename])]
    return [c for c in A if c not in B]

if __name__=='__main__':

    utils.check_dir(DIR['summaries'])
    utils.check_dir(DIR['specifics'])
    utils.check_dir(DIR['proposers'])
    utils.check_dir(DIR['withdrawers'])

    metadata = get_metadata()

    #TODO: get metadata range input from settings
    for bill_id in metadata:
        get_pages(bill_id, metadata)
        print bill_id

    missing = check_missing('specifics', END_BILL)
    print missing

    get_pages('1901020')
