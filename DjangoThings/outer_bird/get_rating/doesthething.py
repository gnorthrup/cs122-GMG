import get_rating.tweets
import get_rating.sentiment

def thething(string):
	if len(string) != 0:
		query = tweets.Query(string)
		tweets.collect_tweets(query,600)
		sentiment.nltk_vader(query)
		return str(query.avg_rate)
	else:
		return 'Need query'
