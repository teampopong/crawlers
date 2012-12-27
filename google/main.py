#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import json
import ndocs

def get_list(filepath):
    with open(filepath, 'r') as f:
        doc = json.load(f)
        names = [d['name_kr'] for d in doc]
    return names

filepath = '../election_commission/data/assembly-elected-19.json'
print 'get names for ' + filepath
names = get_list(filepath)
print 'retrieving document numbers from google...'
m = ndocs.as_matrix(names)
print 'write to file...'
ndocs.write_csv(q, m)
print 'done'
