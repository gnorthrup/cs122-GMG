# Sentiment Analysis

import nltk
import csv
import random
import nltk.sentiment.vader as vd
import nltk
import pickle
from nltk.corpus import movie_reviews

lexicon_filename = 'effectwordnet/EffectWordNet.csv'
pos_corpus = 'tagged_reviews/pos'
neg_corpus = 'tagged_reviews/neg'

def lexicon_analysis(query, lexicon_filename):
    '''
    Use EffectWordNet lexicon to classify value of tweet
    Inputs:
        tweets: tweets
        lexicon_filename
    '''
    effect_conversion = {"+Effect": 1, "-Effect": -1, "Null": 0}
    with open(lexicon_filename) as f:
        lex_reader = csv.reader(f, delimiter='\t')
        lexicon = {}
        for row in lex_reader:
            try:
                lexicon[row[2]] = effect_conversion[row[1]]
            except:
                print(row[2], row[1])
    tweets = query.tweets

    for tweet in tweets:
        tweet_score = 0
        for word in tweet.text.lower().split():
            if word in lexicon:
                tweet_score += lexicon[word]
        if tweet_score == 0:
            tweet.rate = 0
        else:
            tweet.rate = tweet_score / abs(tweet_score)

    avg_rating = 0
    num_valenced = 0
    for tweet in tweets:
        avg_rating += tweet.rate
        num_valenced += (tweet.rate != 0)
    query.avg_rate = (avg_rating / float(num_valenced)) * 50 + 50


def train_naive_bayes():
    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    global word_features
    word_features = list(all_words)[:3000]
    featuresets = [(document_features(d), c) for (d, c) in documents]
    train_set, test_set = featuresets[1000:], featuresets[:1000]
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    return classifier


def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

def prob_from_bayes(classifier):
    term_probs =  {}
    prob_dict = classifier._feature_probdist
    cpdist = classifier._feature_probdist
    valence = {'neg': -1, 'pos': +1}

    for (fname, fval) in classifier.most_informative_features(200):
        def labelprob(l):
            return cpdist[l, fname].prob(fval)

        labels = sorted([l for l in classifier._labels
            if fval in cpdist[l, fname].samples()], key=labelprob)
        if len(labels) == 1:
            continue
        l0 = labels[0]
        l1 = labels[-1]
        if cpdist[l0, fname].prob(fval) == 0:
            ratio = 'INF'
        else:
            ratio = '%8.1f' % (cpdist[l1, fname].prob(fval) /
                    cpdist[l0, fname].prob(fval))
        key = fname[fname.find("(")+1:fname.find(")")]
        term_probs[key] = valence[l0] * float(ratio)

    return term_probs

def create_bayesian_dict(filename='movie_terms.p'):
    with open(filename,"wb") as f:
        pickle.dump(prob_from_bayes(train_naive_bayes()), f)


def nltk_vader(query, category = None):
    if category == 'movie':
        with open('get_rating/movie_terms.p', "rb") as f:
            movie_terms = pickle.load(f)
    sid = vd.SentimentIntensityAnalyzer()
    avg_rating = 0
    num_valenced = 0
    best_score = 0
    worst_score = 0
    X_max = 85
    X_min = 15
    for tweet in query.tweets:
        scores = sid.polarity_scores(tweet.text)
        tweet.rate = scores['compound']
        if category == 'movie':
            for word in tweet.text.lower().split():
                if word in movie_terms:
                    tweet.rate += movie_terms[word]
        tweet.norm_rate = (((tweet.rate * 50 + 50) - X_min) / (X_max - X_min)) * 100
        if tweet.rate > best_score:
            best = tweet
            best_score = tweet.rate
        elif tweet.rate < worst_score:
            worst = tweet
            worst_score = tweet.rate
        avg_rating += tweet.rate
        num_valenced += (tweet.rate != 0)

    if num_valenced == 0:
        pass
    else:
        query.avg_rate = (avg_rating / float(num_valenced)) * 50 + 50
        X_std = (query.avg_rate - X_min) / (X_max - X_min)
        query.avg_rate = X_std * 100
        query.best = best
        query.worst = worst
