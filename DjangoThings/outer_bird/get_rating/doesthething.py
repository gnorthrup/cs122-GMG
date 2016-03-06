import get_rating.tweets
import get_rating.sentiment
import numpy as np

def thething(string):
	if len(string) != 0:
		query = get_rating.tweets.Query(string)
		get_rating.tweets.collect_tweets(query,600)
		get_rating.sentiment.nltk_vader(query)
		return (str(np.round(query.avg_rate,2)),query.best.text,query.worst.text)
	else:
		return ('','','')
