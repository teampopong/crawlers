#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs


REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"


def setup_oauth1(keys):
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(keys['consumer_key'], client_secret=keys['consumer_secret'])
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(keys['consumer_key'],
                   client_secret=keys['consumer_secret'],
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth1(keys):
    if not keys['oauth_token']:
        keys['oauth_token'], keys['oauth_token_secret']\
                = setup_oauth1(keys)
        print '\nInput the keys below to twitter/settings.py'
        import pprint; pprint.pprint(keys)
        import sys; sys.exit()

    oauth = OAuth1(keys['consumer_key'],
                client_secret=keys['consumer_secret'],
                resource_owner_key=keys['oauth_token'],
                resource_owner_secret=keys['oauth_token_secret'])
    return oauth
