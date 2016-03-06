import numpy as np
import matplotlib.pyplot as plt 

def create_hist(query, category = None):
    '''
    Plots a histogram of tweet ratings. query.find_avg_rate() must have
    been called already, and if is_movie = True, query.find_conventinal_ratings()
    must be called. 
    '''
    rates = [t.rate for t in query.tweets]
    plt.hist(rates)
    plt.xlabel('Ratings')
    plt.title('Distribution of {} Sentiments'.format(query.term))
    plt.grid(True)
    plt.axvline(query.avg_rate, color = 'g', label = 'Average Rating', linestyle = 'dashed', linewidth=2)
    plt.xlim([0, 1])
    plt.gcf().subplots_adjust(right=0.75)
    if category == 'movie':
        plt.axvline(query.tomato_rating, color = 'r', label = 'Rotten Tomato Rating', linestyle='dashed', linewidth=2)
        plt.axvline(query.tomato_audiance_score, color= 'b', label = 'Rotten Tomato Audiance Score', linestyle='dashed', linewidth=2)
    if category == 'book':
        plt.axvline(query.good_reads_rating, color = 'r', label = 'GoodReads Rating', linestyle='dashed', linewidth=2)
    if category == 'album':
        plt.axvline(query.pitchfork_rating, color = 'r', label = 'Pitchfork Rating', linestyle = 'dashed', linewidth=2)
    plt.legend(bbox_to_anchor=(1., 1),loc=2, borderaxespad=0, fontsize='small')

    return plt


