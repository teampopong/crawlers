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

def get_most_retweet_count():

    oauth = get_oauth()

    # load 'since_id' from a file written in old times
    f = open('twitter_since_id.log', 'r+')
    since_id = f.readline()
    latest_id = since_id

    # request tweets API
    req_params = {'user_id': '1484174988', 'count':'200', 'since_id': since_id}
    r= requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json", auth=oauth, params=req_params)
    json_obj = r.json()

    # insert 'id_str', 'retweet_count' to the Dict data structure
    result_request_tweet = {}
    for x in json_obj:
        result_request_tweet[x['id_str']] = x['retweet_count']

    # sort by retweet_count
    sorted_json_list = sorted(result_request_tweet.items(), key=itemgetter(1), reverse=True)
    print sorted_json_list

    # save latest_tweet_id to a file as since_id
    if len(result_request_tweet) != 0:
        latest_id = sorted(result_request_tweet, reverse=True)[0]
    print "latest_id : %s"%latest_id
    f.seek(0)
    f.write(latest_id)
    f.close()

    return sorted_json_list[0][0]
