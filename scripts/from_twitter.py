#!/usr/bin/env python

import urllib
import httplib
import base64
import json
import ast
import pprint
import constants

### UTILS ###

def authenticate():
    '''
    Used to auntheticate. Consumer ket and scret are
    pre-defined. Returns the header if succesful else
    exits.
    '''
    CONSUMER_KEY=constants.CONSUMER_KEY
    CONSUMER_SECRET=constants.CONSUMER_SECRET

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


def get_tweets_from_json(json_data):
    """
    Takes a list
    and returns a list of tweet objects
    """
    tweets = list()
    list_of_tweets = json.loads(json_data)

    for t in list_of_tweets:
        tweets.append(tweet(t))

    return tweets

##################################### END UTILS ########################################


class twitter():

    def __init__(self, screename, conn=None):
        """
        Expects the screen_name for which, the tweets will
        be fetched.
        """
        self._screename = screename
        self._conn = conn

    def _set_conn(self):
        """
        Sets the HTTP Connection with twitter api end point.
        Close the connection, when usage is done
        """
        self._conn = httplib.HTTPSConnection("api.twitter.com")
        return self._conn

    def _close_conn():
        if conn:
            self._conn.close()

    def _fetch_tweets(self,authentication_token, counts):
        """
        Fetches <count> no. of tweets.
        Loads it into json and returns the json object.
        """
        try:
            api_url = "/1.1/statuses/user_timeline.json?screen_name=%s&count=%s"
            request = self._conn.request("GET", api_url % (self._screename, counts),
                                         "", authentication_token)

            response = self._conn.getresponse()
            data_received = response.read()

            return data_received

        except:
            print "Some error occurred..."

# add all the attributes as properties
# will make it more efficient
# shouldn't calculate if things have
# been calculated once
class tweet():
    def __init__(self, json_data):
        """
        Initialize the object with the tweet data(json)
        """
        self._tweet = json_data

    def _get_user(self):
        """
        Returns a dict with user details.
        Eg followers, location, screen_name etc
        """
        return self._tweet['user']

    def _get_screen_name(self):
        """
        Method to give the screen name for the tweet
        """
        user = self._get_user()
        return user['screen_name']

    def _get_location(self):
        """
        Returns location of the user
        """
        return self._get_user()['location']

    def _get_retweets(self):
        """
        Gives the count of retweets
        """
        return int(self._tweet['retweet_count'])

    def _get_tweet(self):
        """
        Gives the tweet. Could be a link or text
        """
        return self._tweet['text']

    def _get_urls(self):
        """
        Returns usable URLs (list o f URLs).
        The URLS can be directly used by urllib etc
        """
        usable_urls = list()
        urls = self._tweet['entities']['urls']

        for url in urls:
            usable_url = url['expanded_url']
            usable_url = usable_url.replace(" ","") # trimming
            usable_urls.append(usable_url)

        return usable_urls

    def _print_details(self):
        """
        Print the properties(not yet props)
        """
        print "Screen Name: " + self._get_screen_name()
        print "Tweet: " + self._get_tweet()
        print "Retweets: " + str(self._get_retweets())
        print "URLs: " + ", ".join(self._get_urls())

# Test
if __name__ == "__main__":
    # use authenticate to get the token
    token = authenticate()
    # create a twitter obj with screen_name
    tc = twitter("symantec")
    tc._set_conn()
    # Use the auth token and no of counts of tweets
    # for the screen_name(symantec)
    tweets = get_tweets_from_json(tc._fetch_tweets(token, 3))

    for t in tweets:
        t._print_details()
        print "----------------------------------"
