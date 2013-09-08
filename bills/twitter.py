#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
from settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET


REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"


def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(TWITTER_CONSUMER_KEY,
                   client_secret=TWITTER_CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(TWITTER_CONSUMER_KEY,
                client_secret=TWITTER_CONSUMER_SECRET,
                resource_owner_key=TWITTER_OAUTH_TOKEN,
                resource_owner_secret=TWITTER_OAUTH_TOKEN_SECRET)
    return oauth


def post(status):
    oauth = get_oauth()
    requests.post(url="https://api.twitter.com/1.1/statuses/update.json", auth=oauth, data={"status": status})

