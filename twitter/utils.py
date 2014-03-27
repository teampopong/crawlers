#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from datetime import date
import os


def today():
    return str(date.today())

def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_list_to_text(data, filename):
    with open(filename, 'w') as f:
        f.write('\n'.join(str(d) for d in data))
    print "Written to %s" % filename
