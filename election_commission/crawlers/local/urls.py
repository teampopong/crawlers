#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from urllib import urlencode

import static
from static import election_types

baseurl = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml?'

def get_past_election_url(election_id, election_type, city_id, member_type):
    if election_id < 4:
        old_election_type = '0'
        if member_type=='elected':
            statement_id = 'EPEI01_/99'
        elif member_type=='candidates':
            statement_id = 'CPRI03_/00'
        else:
            raise
    else:
        old_election_type = '1'
        if member_type=='elected':
            statement_id = 'EPEI01_/3'
        elif member_type=='candidates':
            statement_id = 'CPRI03_/1'
        else:
            raise
    opts = {
            'electionId': '0000000000',
            'requestURI': '/electioninfo/0000000000/ep/epei01.jsp',
            'electionType': '4',
            'electionCode': election_type,
            'cityCode': '-1',
            'statementId': 'EPEI01_#99',
            'oldElectionType': old_election_type,
            'electionName': '19950627',
            'electionCode': '4'
            }
    url = baseurl + urlencode(opts)
    return url

def get_election_url_base(election_id, election_type):
    # TODO: get list of election_ids and input max(election_ids)
    election_type = static.get_election_type_id(election_type)
    if election_type in election_types.values():
        opts = {
            'electionId': '00%s' % election_id,
            'electionCode': election_type,
            'requestURI': '/electioninfo/00%s/pc/pcri03_ex.jsp' % election_id,
            'statementId': 'PCRI03_#%s' % election_type,
            }
        url = baseurl + urlencode(opts)
    else:
        raise Exception('Election types in [3,4,5,6,10,11]')
    return url
