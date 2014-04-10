#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import requests

import setup
from settings import DATADIR, TWITTER_KEYS, TWITTER_HANDLES
import utils

def get_follower_ids(handle, oauth, filename=None):
    r = requests.get(\
        url='https://api.twitter.com/1.1/followers/ids.json',\
        params={'screen_name': handle}, auth=oauth)

    if r.status_code==200:
        print 'Followers for %s fetched' % handle
        ids = sorted(r.json()['ids'])

        if filename:
            utils.write_list_to_text(ids, filename)
    else:
        ids = []

    return ids


if __name__=='__main__':
    for handle in TWITTER_HANDLES:

        handle_dir = '%s/%s' % (DATADIR, handle)
        filename = '%s/%s-follower-ids.txt' % (handle_dir, utils.today())
        utils.check_dir(handle_dir)

        ids = get_follower_ids(handle,\
                oauth=setup.get_oauth1(keys=TWITTER_KEYS),\
                filename=filename)
