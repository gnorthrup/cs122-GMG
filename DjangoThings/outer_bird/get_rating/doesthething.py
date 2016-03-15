import get_rating.tweets
import get_rating.sentiment
import get_rating.plots
import numpy as np

def thething(string, category, top, bottom):
	if len(string) != 0:
		query = get_rating.tweets.Query(string)
		get_rating.tweets.collect_tweets(query,600)
		if query.try_again:
			return ('Not enough tweets! Please check your spelling and try again.', '', '', '', '')
		get_rating.sentiment.nltk_vader(query, category, top, bottom)
		try:
			get_rating.plots.create_hist(query,category)
		except ValueError:
			print(ValueError)
			return ('Not enought tweets! Please try again', '', '', '', '')
		get_rating.plots.create_cloud(query)
		return (str(np.round(query.avg_rate,2)),query.best.text,query.worst.text,query.top_tweets, query.bottom_tweets)
	else:
		return ('','','','','')
