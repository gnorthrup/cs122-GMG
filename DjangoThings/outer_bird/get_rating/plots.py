import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud 
import re
from PIL import Image

def create_hist(query, category = None):
    '''
    Plots and saves a histogram of tweet ratings

    Inputs:
        query: a Query object
        category: an optional parameter specifying 
            what category the query term is. Default
            value is None, and other possible values 
            are 'movie', 'book', or 'album'
    '''
    rates = [t.norm_rate for t in query.tweets if t.norm_rate != 50]
    if len(rates) == 0:
        query.try_again = True
        return 
    plt.hist(rates,bins=20)
    plt.xlabel('Ratings')
    plt.xlim(-20,120)
    plt.title('Distribution of {} Sentiments'.format(query.term))
    plt.grid(True)
    plt.axvline(query.avg_rate, color = 'g', label = 'Average Rating', linestyle = 'dashed', linewidth=2)
    plt.gcf().subplots_adjust(right=0.75)

    # If the category is a movie, Rotten Tomato ratings will be plotted as vertical dashed lines
    if category == 'movie':
        query.find_movie_rating()
        if query.tomato_rating != None: 
            plt.axvline(query.tomato_rating, color = 'r', label = 'Rotten Tomato Rating', linestyle='dashed', linewidth=2)
        if query.tomato_audiance_score != None:
            plt.axvline(query.tomato_audiance_score, color= 'b', label = 'Rotten Tomato Audiance Score', linestyle='dashed', linewidth=2)
    
    # If the category is a book, GoodReads rating will be plotted as a vertical dashed line
    if category == 'book':
        query.find_book_rating()
        if query.goodreads_rating != None:
            plt.axvline(query.goodreads_rating, color = 'r', label = 'GoodReads Rating', linestyle='dashed', linewidth=2)
    
    # If the category is an album, Pitchfork ratings will be plotted as a vertical dashed line
    if category == 'album':
        query.find_music_rating()
        if query.pitchfork_rating != None:
            plt.axvline(query.pitchfork_rating, color = 'r', label = 'Pitchfork Rating', linestyle = 'dashed', linewidth=2)
    plt.legend(bbox_to_anchor=(1., 1),loc=2, borderaxespad=0, fontsize='small')
    # The figure is saved as the same name, so when each query is made this file is changed. This way the number of files
    # being saved does not accumulate
    plt.savefig('get_rating/static/get_rating/images/hist.png')
    plt.close()
    return

def create_cloud(query):
    '''
    Creates a word cloud based on the frequency of words accompanying a query
    search term in tweets.

    Inputs:
        query: a Query object 
    '''
    stop_words = set(['RT','https','http','co','via','amp'] + query.term.split() + query.term.lower().split() + query.term.title().split() + query.term.upper().split())
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
    # The figure is saved as the same name, so when each query is made this file is changed. This way the number of files
    # being saved does not accumulate
    fig.savefig('get_rating/static/get_rating/images/cloud.png',aspect='normal')
    plt.close()
    return
