import get_rating.tweets
import get_rating.sentiment
import get_rating.plots
import numpy as np

def thething(string, category):
	if len(string) != 0:
		query = get_rating.tweets.Query(string)
		get_rating.tweets.collect_tweets(query,600)
		if query.try_again:
			return ('Not enough tweets! Please try again.', '', '', '')
		get_rating.sentiment.nltk_vader(query)
		try:
			plt = get_rating.plots.create_hist(query,category)
		except:
			return ('Not enought tweets! Please try again', '', '', '')
		get_rating.plots.create_cloud(query)
		return (str(np.round(query.avg_rate,2)),query.best.text,query.worst.text,plt)
	else:
		return ('','','','')
