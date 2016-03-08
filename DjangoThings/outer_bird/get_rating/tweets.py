### Run --sudo pip3 install twitter-- on your VM ###
 
# 4. more validation APIs?
# 6. hist legend  

import tweepy
import twitter
import requests
import json
import bs4
from get_rating.tweets_db import update_tweets_table

ACCESS_TOKEN = '4870966822-1zGNGFWElLkgginMDYWJUGo4UKgsxOJcsMUScFS'
ACCESS_SECRET = 'DH9WLbu1WGu3i2GgyTRC4Y3hgyJCbGUo9a1UAGGvedIqp'
CONSUMER_KEY = 'Kn5n5ZQjYcRgAyQ57iBH6AZrT'
CONSUMER_SECRET = 'LR370Rd5T6bHxbkMwCF2lGg7lMhHpqx4nn4st1yTNQmhFwe0JM'

GOOD_READS_KEY = 'atNmEak6yg8LAf2OQdBkIQ'
GOOD_READS_SECRET = 'CjVgWwW5hbyZk9apGet26knMy4YSYvqK5Np5gIZCVCM'

# This class will store information about a single tweet,
# such as the text and the rating we will assign it.
class Tweet(object):
    def __init__(self, text, date, i_d):
        self.text = text.replace('"', "'")
        self.date = date
        self.id = i_d
        self.rate = None
        self.norm_rate = None

    def __eq__(self, other): 
        #is_equal = isinstance(other, self.__class__) and \
        #           self.text == other.text and \
        #           self.date == other.date and \
        #           self.user == other.user
        #return is_equal
        return self.id == other.id

    #def __ne__(self, other):
    #    return not self.__eq__(other)

    def __hash__(self):
        return 0

# This class will contain information about a specific search
# somebody does. The term attribute will be the movie title
# (or something else) of interest and the tweets attribute
# will be a list of Tweet objects with content related to the
# term.
class Query(object):
    def __init__(self, term, artist = None):
        self.term = term
        self.tweets = set()
        self.num_tweets = 0
        self.artist = artist
        self.avg_rate = None
        self.tomato_rating = None
        self.tomato_audiance_score = None
        self.imdb_rating = None
        self.goodreads_rating = None
        self.pitchfork_rating = None
        self.try_again = False

    def add_tweet(self, tweet):
        self.tweets.add(tweet)
        self.num_tweets += 1
        return

    def find_movie_rating(self):
        url = 'http://www.omdbapi.com/?'
        parameters = '&tomatoes=true&r=json'
        title_words = self.term.split()
        title = 't={}'.format('+'.join(title_words))
        url += title + parameters

        r = requests.get(url)
        read = r.text
        info_dict = json.loads(read)
        self.tomato_rating = int(info_dict['tomatoMeter']) / 100
        self.tomato_audiance_score = int(info_dict['tomatoUserMeter']) / 100
        self.imdb_rating = float(info_dict['imdbRating']) / 10
        return

    def find_book_rating(self):
        key = GOOD_READS_KEY 
        url = 'https://www.goodreads.com/search.xml?key={}&q={}'.format(key, self.term)
        r = requests.get(url)
        read = r.text
        soup = bs4.BeautifulSoup(read, 'html5lib')
        rating = soup.body.work.average_rating.contents[0]
        self.goodreads_rating = float(rating) / 5
        return

    def find_music_rating(self):
        p = pitchfork.search(self.term, self.artist)
        self.pitchfork_rating = p / 10

def stream_tweets(num_tweets, update_db = [], query = None):
    '''
    Inputs:
        num_tweets: the number of tweets to stream from twitter
                    default value is NA, so the number of tweets
                    collected is not limited
        update_db: an optional parameter. If update_db is not equal to
                    [] the function will load the tweets into a database.
                    If specified, must be a list where the first entry is
                    the name of the database and the second entry is the
                    name of the table for the tweets to be saved in.
        query: an optional parameter of a Query object. Default value is
                None.
    '''
    oauth = twitter.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    twitter_stream = twitter.TwitterStream(auth=oauth)
    if query == None:
        iterator = twitter_stream.statuses.sample(language = 'en')
    else:
        iterator = twitter_stream.statuses.filter(track = query.term, language = 'en')
    count = 0
    for tweet in iterator:
        if count == num_tweets:
            break
        count += 1
        print(count)
        text = tweet.get('text', '')
        date = tweet.get('created_at', '')
        if update_db != []: 
            update_tweets_table(update_db[0], update_db[1], update_db[2], text.replace('"', "'"), date)
        if query != None:    
            query.add_tweet(Tweet(text, date))
    return

def search_tweets(query, num_tweets, max_id = None, update_db = []):
    '''
    update_db: an optional parameter. If update_db is not equal to
                    [] the function will load the tweets into a database.
                    If specified, must be a list where the first entry is
                    the name of the database and the second entry is the
                    name of the table for the tweets to be saved in. The
                    third entry in the list is a list of column names.
    '''
    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    #if we want to add a time limit specify timeout parameter in API
    #class (in secons). Default value is 60 sec.
    api = tweepy.API(auth)

    tweets = api.search(q=query.term, lang = 'en', max_id = max_id, count = num_tweets)
    min_id = float('inf')
    for status in tweets:
        tweet = Tweet(status.text, status.created_at, status.id)
        query.add_tweet(tweet)
        if tweet.id < float('inf'):
            min_id = tweet.id
        if update_db != []:
            update_tweets_table(update_db[0], update_db[1], update_db[2], tweet.text.replace('"', "'"), tweet.created_at)
    return min_id - 1 

def collect_tweets(query, total_tweets):
    max_id = None
    n = total_tweets // 100
    for i in range(n):
    #while query.num_tweets < total_tweets:
        try:
            max_id = search_tweets(query, 100, max_id = max_id)
        except:
            query.try_again = True
            break
    return 