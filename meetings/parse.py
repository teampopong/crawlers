#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import dateutil.parser
from glob import glob
import os

from popong_doclib import meeting
from popong_doclib import utils # v0.2


def parse_meeting(filebase, pdfdir='/popong/data/meeting-docs/national'):
    pdffile = '%s/%s.pdf' % (pdfdir, filebase)
    xmlroot = utils.pdf2xml(pdffile)
    sections = meeting.national.get_sections(xmlroot)
    meeting_dict = meeting.parse(sections)
    meeting_dict_to_file(meeting_dict, filebase)
    print filebase

def get_filebases(date=None, assembly_id=19, pdfdir='/popong/data/meeting-docs/national'):
    if not date:
        date = '*'
    targetdir = '%s/%s/%s/*.pdf' % (pdfdir, assembly_id, date)
    targetfiles = glob(targetdir)
    return [f.split(os.sep, 5)[-1].strip('.pdf') for f in targetfiles]

def meeting_dict_to_file(meeting_dict, filebase,\
                         datadir='/popong/data/meetings/national'):
    types = ['dialogue', 'votes', 'attendance'] # TODO: parse_reports
    for type_ in types:
        if meeting_dict.get(type_):
            filename = "%s/%s/%s.json" % (datadir, type_, filebase)
            utils.write_json(meeting_dict[type_], filename)


if __name__=='__main__':
    from datetime import date, timedelta
    import sys
    if len(sys.argv) > 1:
        files = get_filebases(sys.argv[1])
    else:
        ndates = 30
        dates = [(date.today() - timedelta(d)).isoformat() for d in range(ndates)]
        files = sum((get_filebases(date) for date in dates), [])
    for f in files:
        parse_meeting(f)
