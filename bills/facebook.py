#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from json import dumps
from oauthlib.common import urldecode
from requests_oauthlib import OAuth2Session
import requests

from settings import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, FACEBOOK_OAUTH_TOKEN, FACEBOOK_PAGE_ID

AUTHORIZATION_BASE_URL = 'https://www.facebook.com/dialog/oauth'
TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
REDIRECT_URI = 'https://pokr.kr/'
POST_URL = "https://graph.facebook.com/%s/feed"

def facebook_compliance_fix(session):

    def _compliance_fix(r):
        token = dict(urldecode(r.text))
        token['expires_in'] = token['expires']
        token['token_type'] = 'Bearer'
        r._content = dumps(token)
        return r

    session.register_compliance_hook('access_token_response', _compliance_fix)
    return session


def setup_oauth():
    oauth = OAuth2Session(FACEBOOK_CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["manage_pages","publish_stream"])
    oauth = facebook_compliance_fix(oauth)

    authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
    print 'Please go here and authorize,', authorization_url

    redirect_response = raw_input('Paste the full redirect URL here:')

    token = oauth.fetch_token(TOKEN_URL, client_secret=FACEBOOK_CLIENT_SECRET,
                        authorization_response=redirect_response)

    return token["access_token"]


def get_oauth():
    oauth = OAuth2Session(FACEBOOK_CLIENT_ID, redirect_uri=REDIRECT_URI)
    oauth = facebook_compliance_fix(oauth)
    return oauth


def post(message):
    oauth = get_oauth()
    oauth.post(url=POST_URL % FACEBOOK_PAGE_ID, data={"message":message,"access_token":FACEBOOK_OAUTH_TOKEN})

