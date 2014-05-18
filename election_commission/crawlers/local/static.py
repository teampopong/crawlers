#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from utils import get_json

url_json_base = 'http://info.nec.go.kr/bizcommon/selectbox'

election_ids = {
    '1': '19950627',
    '2': '19980604',
    '3': '20020613',
    '4': '20060531',
    '5': '20100602',
    '6': '20140604'
}

election_types = {
    'province_governor'         : 3,
    'province_member'           : 5,
    'municipality_governor'     : 4,
    'municipality_member'       : 6,
    'province_proportional'     : 8,
    'municipality_proportional' : 9,
    'education_member'          : 10,
    'education_governor'        : 11
}

short_election_types = {''.join(k[0] for k in key.split('_')): value\
    for key, value in election_types.items()}

reversed_election_types = {v:k for k,v in election_types.items()}

def get_election_id(election_id):
    election_id = int(election_id)
    if election_id < election_ids['1']:
        try:
            return election_ids[str(election_id)]
        except KeyError:
            return
    else:
        return election_id

def get_election_type_id(election_type):
    if isinstance(election_type, int):
        return election_type
    else:
        try:
            return election_types[election_type]
        except KeyError:
            return short_election_types[election_type]

def get_election_type_name(election_type):
    if not election_type:
        raise Exception(\
                'For local candidates you must specify a "level (-l)" flag.')
    if election_type in election_types.keys():
        return election_type
    elif election_type in short_election_types.keys():
        election_type = short_election_types[election_type]
    return reversed_election_types[election_type]

def get_valid_election_type_ids(election_id):
    election_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSubElectionTypeJson.json?electionId=0000000000&electionCode=%s&electionType=4' % election_id
    codes = [i['CODE'] for i in get_json(election_json)['body']]
    return codes

def url_city_ids_json(election_id, election_type):
    if int(election_id) < 4:
        election_id = get_election_id(election_id)
        election_type = get_election_type_id(election_type)
        return '%s/selectbox_cityCodeBySgJson_GuOld.json?electionId=0000000000'\
            '&electionCode=%s' % (url_json_base, election_id)
    else:
        election_id = get_election_id(election_id)
        election_type = get_election_type_id(election_type)
        return '%s/selectbox_cityCodeBySgJson_Old.json?electionId=0000000000'\
            '&subElectionCode=%s&electionCode=%s'\
            % (url_json_base, election_type, election_id)

def url_election_types_json(election_id):
    return '%s/selectbox_getSubElectionTypeJson.json?electionId=0000000000'\
        '&electionType=4&electionCode=%s' % (url_json_base, election_id)

def url_town_ids_json(election_id, election_type, city_id):
    return '%s/selectbox_getSggCityCodeJson_GuOld.json?electionId=0000000000'\
        '&electionName=%s&electionCode=%s&cityCode=%s'\
        % (url_json_base, election_id, election_type, city_id)
