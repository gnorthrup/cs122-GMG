#Sentiment Analysis

import nltk
import csv
from tweets import *
lexicon_filename = 'effectwordnet/EffectWordNet.csv'


def lexicon_analysis(tweets,lexicon_filename):
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
            lexicon[row[3]] = effect_conversion[row[2]]

    for tweet in tweets:
        tweet_score = 0
        for word in tweet.text.split():
            if word in lexicon:
                tweet_score += lexicon[word]
        tweet.rate(tweet_score/abs(tweet_score))
