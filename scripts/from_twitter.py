#!/usr/bin/env python

import urllib
import httplib
import base64
import json
import ast

def authenticate():
    '''
    Used to auntheticate. Consumer ket and scret are
    pre-defined. Returns the header if succesful else
    exits.
    '''
    CONSUMER_KEY='tI0bUJuctVgzA82wGYLiQ'
    CONSUMER_SECRET='59GVWA6j7RJt1Ntw2cFi57FS91jzRFIk6lbNzH8Cs8'

    enc_str= base64.b64encode(CONSUMER_KEY+":"+CONSUMER_SECRET)

    conn = httplib.HTTPSConnection("api.twitter.com")

    #Acquiring the access token
    param = urllib.urlencode({'grant_type':'client_credentials'})
    headers = {"Authorization":"Basic "+enc_str,
               "Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}

    conn.request("POST","/oauth2/token/",param,headers)

    response=conn.getresponse()
    payload = response.read()

    ## Converting the payload string to a dictionary
    dic = ast.literal_eval(payload)

    access_token = dic.get("access_token")
    get_headers={"Authorization":"Bearer "+access_token}
    conn.close()

    return get_headers

class twitter():
    def __init__(self, screename, conn=None):
        '''
        Expects the screen_name for which, the tweets will
        be fetched.
        '''
        self._screename = screename
        self._conn = conn

    def _set_conn(self):
        self._conn = httplib.HTTPSConnection("api.twitter.com")
        return self._conn

    def _fetch_tweets(self,authentication_token, counts):
        try:
            print authentication_token
            api_url = "/1.1/statuses/user_timeline.json?screen_name=%s&count=%s"
            print api_url % (self._screename, counts)
            request = self._conn.request("GET", api_url % (self._screename, counts),
                                         "", authentication_token)

            response = self._conn.getresponse()
            data_received = response.read()

            print data_received

        except:
            print "Some error occurred..."

# Test
if __name__ == "__main__":
    token = authenticate()
    tc = twitter("symantec")
    tc._set_conn()
    tc._fetch_tweets(token, 5)
