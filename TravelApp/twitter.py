import requests
import json
import tweepy
from tweepy.auth import OAuthHandler
from textblob import TextBlob
from collections import OrderedDict

def getSentiments(query):
    auth = OAuthHandler('XRCnQ49KVWgy0IsN5QYBTn5Zm', 'P6UwYNbfboKQfrr51P3HLjp88Mq32SxNcQt7zsFKDdAZdXrAoW')
    auth.set_access_token('912853951984238592-BODZqgKvgD0QdKD5Rz1grMGPCDFiZm4', 'proz3qXFAR7Ie8YOylG86z0uERL8orw0HcClAA2X4CN6t')

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    public_tweets = []

    chartData = OrderedDict()
    total_pos = 0
    total_neg = 0
    total_neu = 0

    total_senti = 0

    for tweet in tweepy.Cursor(api.search, q=query, result_type="recent", tweet_mode="extended", lang="en").items(20):
        # print(tweet.full_text)
        blob = TextBlob(tweet.full_text)
        senti = blob.sentiment.polarity
        total_senti += senti
        sub = float("{0:.2f}".format(blob.sentiment.subjectivity))
        if senti>0.1:
            senti_analysis = 'Positive'
            total_pos += 1
        elif senti<-0.1:
            senti_analysis = 'Negative'
            total_neg += 1
        else:
            senti_analysis = 'Neutral'
            total_neu += 1
        public_tweets.append({'tweet':tweet, 'subjectivity':sub, 'senti': senti, 'senti_analysis':senti_analysis})
        chartData[tweet.user.screen_name] = senti

    # print(public_tweets)
    return total_senti/2 
