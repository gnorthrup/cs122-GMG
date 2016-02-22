#Sentiment Analysis

import nltk
import csv
import os
import string
import nltk.sentiment.vader as vd
from tweets import *

lexicon_filename = 'effectwordnet/EffectWordNet.csv'
pos_corpus = 'tagged_movies/pos'
neg_corpus = 'tagged_movies/neg'


def lexicon_analysis(query,lexicon_filename):
    '''
    Use EffectWordNet lexicon to classify value of tweet
    Inputs:
        tweets: tweets
        lexicon_filename
    '''
    effect_conversion = {"+Effect": 1, "-Effect": -1, "Null": 0}
    with open(lexicon_filename) as f:
        lex_reader = csv.reader(f,delimiter='\t')
        lexicon = {}
        for row in lex_reader:
            try:
                lexicon[row[2]] = effect_conversion[row[1]]
            except:
                print(row[2],row[1])
    tweets = query.tweets

    for tweet in tweets:
        tweet_score = 0
        for word in tweet.text.lower().split():
            if word in lexicon:
                tweet_score += lexicon[word]
        if tweet_score == 0:
            tweet.rate = 0
        else:
            tweet.rate = tweet_score/abs(tweet_score)

    avg_rating = 0
    num_valenced = 0
    for tweet in tweets:
        avg_rating += tweet._rate
        num_valenced += (tweet._rate != 0)
    query.avg_rate = (avg_rating/float(num_valenced)) * 50 + 50

def train_naive_bayes(query,pos_corpus,neg_corpus):
    rootdir = os.path.abspath(pos_corpus)
    pos_rev = []
    for l, s, files in os.walk(rootdir):
        for file in files:
            with open(pos_corpus+'/'+file) as f:
                pos_rev.append((f.read().translate(None, string.punctuation), 'positive'))

    rootdir = os.path.abspath(neg_corpus)
    neg_rev = []
    for l, s, files in os.walk(rootdir):
        for file in files:
            with open(neg_corpus+'/'+file) as f:
                neg_rev.append((f.read().translate(None, string.punctuation), 'negative'))

    reviews = []
    for (words, sentiment) in pos_rev + neg_rev:
        words_filtered = [word.lower() for word in words.split() if len(word) >= 3]
        reviews.append((words_filtered, sentiment))

    all_words = []
    for (words, sentiment) in reviews:
        all_words.extend(words)
    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()

def nltk_vader(query):
    sid = vd.SentimentIntensityAnalyzer()
    for tweet in query.tweets:
        scores = sid.polarity_scores(tweet.text)
        tweet.rate = scores['compound']

    avg_rating = 0
    num_valenced = 0
    for tweet in query.tweets:
        avg_rating += tweet._rate
        num_valenced += (tweet._rate != 0)
    print(avg_rating)
    print(num_valenced)
    if num_valenced == 0:
        pass
    else:
        query.avg_rate = (avg_rating/float(num_valenced)) * 50 + 50
