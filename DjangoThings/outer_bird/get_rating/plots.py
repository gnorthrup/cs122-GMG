import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud 
import re

def create_hist(query, category = None):
    '''
    Plots a histogram of tweet ratings. query.find_avg_rate() must have
    been called already, and if is_movie = True, query.find_conventinal_ratings()
    must be called. 
    '''
    rates = [t.norm_rate for t in query.tweets if t.norm_rate != 50]
    plt.hist(rates,bins=20)
    plt.xlabel('Ratings')
    plt.title('Distribution of {} Sentiments'.format(query.term))
    plt.grid(True)
    plt.axvline(query.avg_rate, color = 'g', label = 'Average Rating', linestyle = 'dashed', linewidth=2)
    plt.gcf().subplots_adjust(right=0.75)
    if category == 'movie':
        query.find_movie_rating()
        plt.axvline(query.tomato_rating, color = 'r', label = 'Rotten Tomato Rating', linestyle='dashed', linewidth=2)
        plt.axvline(query.tomato_audiance_score, color= 'b', label = 'Rotten Tomato Audiance Score', linestyle='dashed', linewidth=2)
    if category == 'book':
        query.find_book_rating()
        plt.axvline(query.good_reads_rating, color = 'r', label = 'GoodReads Rating', linestyle='dashed', linewidth=2)
    if category == 'album':
        query.find_music_rating()
        plt.axvline(query.pitchfork_rating, color = 'r', label = 'Pitchfork Rating', linestyle = 'dashed', linewidth=2)
    plt.legend(bbox_to_anchor=(1., 1),loc=2, borderaxespad=0, fontsize='small')
    plt.savefig('get_rating/static/get_rating/images/hist.png')
    plt.close()
    return

def create_cloud(query):
    stop_words = set(['RT','https','http','co','via'] + query.term.split() + query.term.lower().split())
    text = ''
    for t in query.tweets:
        tweet_stripped = [word for word in re.findall(r"[\w']+",t.text) if word not in stop_words]
        text += ' '.join(tweet_stripped) + ' '

    cloud = WordCloud().generate(text)
    plt.imshow(cloud)
    plt.savefig('get_rating/static/get_rating/images/cloud.png')
    plt.close()
    return
