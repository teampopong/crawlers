#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import pandas as pd

from settings import BASEURL, LIST_DATA, DIR
import utils

def get_urlmap():
    with open(LIST_DATA, 'r') as f:
        data = pd.read_csv(f)
        print data
    return zip(data['bill_id'], data['link_id'], data['has_summaries'])

if __name__=='__main__':

    utils.check_dir(DIR['summaries'])
    utils.check_dir(DIR['specifics'])
    utils.check_dir(DIR['proposers'])
    utils.check_dir(DIR['withdrawers'])

    urlmap = get_urlmap()

    for bill_id, link_id, has_summaries in urlmap:
        # 상세내역
        outp = '%s/%s.html' % (DIR['specifics'], bill_id)
        utils.get_webpage(BASEURL['specific'] + link_id, outp)

        # 요약
        if has_summaries==1:
            outp = '%s/%s.html' % (DIR['summaries'], id)
            utils.get_webpage(BASEURL['summary'] + link_id, outp)

        # 제안자명단
        outp = '%s/%s.html' % (DIR['proposers'], bill_id)
        utils.get_webpage(BASEURL['proposer_list'] + link_id, outp)

        # 철회요구자명단
        outp = '%s/%s.html' % (DIR['withdrawers'], bill_id)
        utils.get_webpage(BASEURL['withdrawers'] + link_id, outp)

        print bill_id
