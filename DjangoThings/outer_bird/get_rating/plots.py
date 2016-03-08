import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud 
import re
from PIL import Image

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
    if category == 'Movie':
        query.find_movie_ratingss()
        plt.axvline(query.tomato_rating, color = 'r', label = 'Rotten Tomato Rating', linestyle='dashed', linewidth=2)
        plt.axvline(query.tomato_audiance_score, color= 'b', label = 'Rotten Tomato Audiance Score', linestyle='dashed', linewidth=2)
    if category == 'Book':
        query.find_book_rating()
        plt.axvline(query.good_reads_rating, color = 'r', label = 'GoodReads Rating', linestyle='dashed', linewidth=2)
    if category == 'Artist, Album':
        query.find_music_rating()
        plt.axvline(query.pitchfork_rating, color = 'r', label = 'Pitchfork Rating', linestyle = 'dashed', linewidth=2)
    plt.legend(bbox_to_anchor=(1., 1),loc=2, borderaxespad=0, fontsize='small')
    plt.savefig('get_rating/static/get_rating/images/hist.png')
    plt.close()
    return

def create_cloud(query):
    stop_words = set(['RT','https','http','co','via','amp'] + query.term.split() + query.term.lower().split() + query.term.title().split())
    text = ''
    for t in query.tweets:
        tweet_stripped = [word for word in re.findall(r"[\w']+",t.text) if word not in stop_words]
        text += ' '.join(tweet_stripped) + ' '

    twitter_mask = np.array(Image.open('get_rating/static/get_rating/images/mask.jpg'))
    twitter_mask = np.abs(twitter_mask - 1)
    cloud = WordCloud(mask=twitter_mask).generate(text)    
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(cloud)
    fig.savefig('get_rating/static/get_rating/images/cloud.png',aspect='normal')
    return
