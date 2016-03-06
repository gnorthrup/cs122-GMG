import get_rating.tweets
import get_rating.sentiment

def thething(string):
	if len(string) != 0:
		query = get_rating.tweets.Query(string)
		get_rating.tweets.collect_tweets(query,600)
		get_rating.sentiment.nltk_vader(query)
		return str(query.avg_rate)
	else:
		return ''
