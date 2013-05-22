#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd

from settings import BASEURL, DIR, HTML_FIELDS
import utils

def get_metadata(assembly_id, range=None):
    meta = {}
    meta_data = '%s/%d.csv' % (DIR['meta'], assembly_id)
    with open(meta_data, 'r') as f:
        if range:
            data = pd.read_csv(f)[range[0]:range[1]]
        else:
            data = pd.read_csv(f)
    for d in zip(data['bill_id'], data['link_id'], data['has_summaries']):
        meta[d[0]] = (d[1], d[2])
    return meta

def get_page(assembly_id, bill_id, link_id, field):
    outp = '%s/%s/%s.html' % (DIR[field], assembly_id, bill_id)
    if not os.path.isfile(outp):
        utils.get_webpage('%s%s' % (BASEURL[field], link_id), outp)

def get_summaries(assembly_id, bill_id, link_id, has_summaries):
    if has_summaries==1:
        outp = '%s/%s/%s.html' % (DIR['summaries'], assembly_id, bill_id)
        if not os.path.isfile(outp):
            utils.get_webpage('%s%s' % (BASEURL['summaries'], link_id), outp)

def get_html(assembly_id, range=None):
    for field in HTML_FIELDS:
        utils.check_dir('%s/%s' % (DIR[field], assembly_id))

    if range:
        metadata = get_metadata(assembly_id, range=range)
    else:
        metadata = get_metadata(assembly_id)

    #TODO: get metadata range input from settings
    for bill_id in metadata:
        link_id, has_summaries = metadata[bill_id]
        for field in HTML_FIELDS[:-1]:
            get_page(assembly_id, bill_id, link_id, field)
        get_summaries(assembly_id, bill_id, link_id, has_summaries)

        sys.stdout.write('%s\t' % bill_id)
        sys.stdout.flush()
