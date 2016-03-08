import get_rating.tweets
import get_rating.sentiment
import get_rating.plots
import numpy as np

def thething(string, category):
	if len(string) != 0:
		query = get_rating.tweets.Query(string)
		get_rating.tweets.collect_tweets(query,600)
		get_rating.sentiment.nltk_vader(query)
		plt = get_rating.plots.create_hist(query,category)
		get_rating.plots.create_cloud(query)
		return (str(np.round(query.avg_rate,2)),query.best.text,query.worst.text,plt)
	else:
		return ('','','','')
