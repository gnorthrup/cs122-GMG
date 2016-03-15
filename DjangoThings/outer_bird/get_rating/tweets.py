import tweepy
import twitter
import requests
import json
import bs4
import pitchfork 
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
        return self.id == other.id

    # This hash function allows tweets to be stored in a 
    # set in the Query class. 
    def __hash__(self):
        return 0

# This class will contain information about a specific search
# somebody does. The term attribute will be the query of 
# interest and the tweets attribute will be a set of 
# Tweet objects with content related to the term.
class Query(object):
    def __init__(self, term):
        self.term = term
        self.tweets = set()
        # The num_tweets attribute was used to referece
        # the number of tweets that were added and the number
        # of tweets in a set to make sure that the unique
        # tweets are aquired with each Twitter API connection. 
        self.num_tweets = 0

        self.avg_rate = None

        # These attributes will be set as conventional
        # ratings to compare the twitter sentiment analysis
        # to if the if the query category is appropriate.
        self.tomato_rating = None
        self.tomato_audiance_score = None
        self.goodreads_rating = None
        self.pitchfork_rating = None

        # If something goes wrong with the query with 
        # collecting tweets, this attribute will be set
        # to True and the user will be prometed to try 
        # again
        self.try_again = False

    def add_tweet(self, tweet):
        '''
        Adds a Tweet object related to a query
        to the set of tweets and adds one to the 
        num_tweet count 
        '''
        self.tweets.add(tweet)
        self.num_tweets += 1
        return

    def find_movie_rating(self):
        '''
        Collects Rotten Tomato critic rating and 
        Rotten Tomato Audiance Score to compare
        to the sentiment analysis if the query is
        a movie
        '''
        url = 'http://www.omdbapi.com/?'
        parameters = '&tomatoes=true&r=json'
        title_words = self.term.split()
        title = 't={}'.format('+'.join(title_words))
        url += title + parameters
        r = requests.get(url)
        read = r.text
        info_dict = json.loads(read)

        # If the user tried to categorize a query as a movie but
        # the query term is not in Rotten Tomatoes, the program will
        # not be terminated, but no critic reviews will be displayed.
        try:
            self.tomato_rating = int(info_dict['tomatoMeter'])
            self.tomato_audiance_score = int(info_dict['tomatoUserMeter']) 
        except:
            return
        return

    def find_book_rating(self):
        '''
        Collects GoodReads critic ratings to compare
        to the sentiment analysis if the query is
        a book
        '''
        key = GOOD_READS_KEY 
        url = 'https://www.goodreads.com/search.xml?key={}&q={}'.format(key, self.term)
        r = requests.get(url)
        read = r.text
        soup = bs4.BeautifulSoup(read, 'html5lib')

        # If the user tried to categorize a query as a book but
        # the query term is not in GoodReads, the program will
        # not be terminated, but no critic reviews will be displayed.
        try:
            rating = soup.body.work.average_rating.contents[0]
        except:
            return
        self.goodreads_rating = float(rating) * 20
        return

    def find_music_rating(self):
        '''
        Collects Pitchfork critic ratings to compare
        to the sentiment analysis if the query is
        an artist and album 
        '''
        if ',' not in self.term:
            return
        artist = self.term.split(',')[0].strip()
        album = self.term.split(',')[1].strip()

        # If the user tried to categorize a query as a book but
        # the query term is not in GoodReads, the program will
        # not be terminated, but no critic reviews will be displayed.
        try:
            p = pitchfork.search(album, artist)
        except:
            return
        self.pitchfork_rating = p.score() * 10
        return 

def stream_tweets(num_tweets, update_db = [], query = None):
    '''
    Uses the twitter streaming API to continuously collect tweets
    based on a query object

    Inputs:
        num_tweets: streaming will stop after this number of tweets are
            collected from Twitter
        update_db: an optional parameter. If update_db is not equal to
                [] the function will load the tweets into a database.
                If specified, must be a list where the first entry is
                the name of the database and the second entry is the
                name of the table for the tweets to be saved in.
                *Note that this function has this utility but it was not incorported
                *into the functionality of the project
        query: an optional parameter of a Query object. If not specified, the 
            default value of None will collect all tweets streaming from Twitter
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
    Uses the twitter search API to collect tweets based on a query object.

    Inputs: 
        query: a Query object
        num_tweets: the desired number of tweets to be collected from Twitter.
                    The connection will time out after 60 seconds if the specified
                    amount is not attained, so num_tweets will not always be attained. 
                    Note that according the API limits, the maximum num_tweets is 
                    100. If a larger number is specified only 100 will be returned.
        max_id: Default value is None. If specified, no tweets with greater IDs
                    (corresponding to tweets made at a later time) will be collected 
        update_db: an optional parameter. If update_db is not equal to
                    [] the function will load the tweets into a database.
                    If specified, must be a list where the first entry is
                    the name of the database and the second entry is the
                    name of the table for the tweets to be saved in. The
                    third entry in the list is a list of column names.
                    *Note that this function has this utility but it was not incorported
                    *into the functionality of the project

    Returns:
        The maximum id for subsequent API connections in order for connections to 
        collect distinct tweets
    '''
    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
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
    # min_id - 1 will be thee maximum tweet ID for subsequent API connections.
    return min_id - 1 

def collect_tweets(query, total_tweets):
    '''
    This function works around the search API limit of 100 tweets per 
    connection and allowst the user to collect a larger amount of unique tweets. 
    Note that there is still an API limit of 180 connections per 15 minutes.

    Inputs:
        query: a Query object
        total_tweets: an number specifying the total number of tweets desired.
            If this number is not a multiple of 100, it will be rounded to
            the hundreds digit.
    '''
    max_id = None
    n = total_tweets // 100
    for i in range(n):
        try:
            max_id = search_tweets(query, 100, max_id = max_id)
        except:
            query.try_again = True
            break
    return 