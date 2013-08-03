#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from glob import glob
import pandas as pd

from settings import DIR


def read_csv(fname, idx=None):
    with open(fname, 'r') as f:
        csv = pd.read_csv(fname, index_col=idx)
        csv['source'] = fname
        return csv

def combine(data, to_combine):
    unique = to_combine.groupby(level=0).first()
    merged = data.combine_first(unique)
    return merged

if __name__=='__main__':
    mainfile = '%s/popong.csv' % DIR['results']
    data = read_csv(mainfile, idx='ko')

    for fname in glob('%s/*.csv' % DIR['results']):
        if fname!=mainfile:
            to_combine = read_csv(fname, idx='ko')
            data = combine(data, to_combine)

    data.to_csv('glossary.csv', header=False)
