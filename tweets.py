### Run --sudo pip3 twitter-- on your VM ###

import twitter

ACCESS_TOKEN = '4870966822-1zGNGFWElLkgginMDYWJUGo4UKgsxOJcsMUScFS'
ACCESS_SECRET = 'DH9WLbu1WGu3i2GgyTRC4Y3hgyJCbGUo9a1UAGGvedIqp'
CONSUMER_KEY = 'Kn5n5ZQjYcRgAyQ57iBH6AZrT'
CONSUMER_SECRET = 'LR370Rd5T6bHxbkMwCF2lGg7lMhHpqx4nn4st1yTNQmhFwe0JM'

# This class will store information about a single tweet, 
# such as the text and the rating we will assign it.
class Tweet(object):
    def __init__(self, text):
        self._text = text
        self._rate = None

    @property
    def text(self):
        return self._text

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        if not isinstance(rate, (int, float)): 
            raise ValueError ("rate must be a float or int")
        self._rate = rate 

    # What methods would be useful for processing the text of
    # a tweet?

# This class will contain information about a specific search
# somebody does. The term attribute will be the movie title 
# (or something else) of interest and the tweets attribute
# will be a list of Tweet objects with content related to the
# term.
class Query(object):
    def __init__(self, term):
        self._term = term
        self._tweets = []
        self._avg_rate = None

    @property
    def term(self):
        return self._term

    @property 
    def tweets(self):
        return self._tweets

    @property
    def avg_rate(self):
        return self._avg_rate

    @avg_rate.setter
    def avg_rate(self, avg_rate):
        if not isinstance(avg_rate, (int, float)): 
            raise ValueError ("avg_rate must be a float or int")
        self._avg_rate = avg_rate 

    def add_tweet(self, tweet):
        self.tweets.append(tweet)
        return

def stream_tweets(query, num_tweets):
    '''
    Inputs:
        query: a Query object
        num_tweets: the number of tweets to stream from twitter
    '''
    oauth = twitter.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    twitter_stream = twitter.TwitterStream(auth=oauth)
    iterator = twitter_stream.statuses.filter(track = query.term, language = 'en')
    count = 0
    for tweet in iterator:
        if count == num_tweets:
            break
        count += 1
        query.add_tweet(tweet['text'])        
    return

def search_tweets(query, num_tweets):
    oauth = twitter.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    
    conn = twitter.Twitter(auth = oauth)
    results = conn.search.tweets(q=query.term, lang = 'en', count = num_tweets)
    for status in results['statuses']:
        tweet = Tweet(status['text'])
        query.add_tweet(tweet)
    return


sample_query = Query('The Revenant')
search_tweets(sample_query, 50)
# Gabe, to access the text from the tweets:
# sample_query.tweets[i].text for 0 <= i <= 37
# (I'm not sure why it only returned 38 results when I requested 50)  
