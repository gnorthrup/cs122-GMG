import tweets
import sentiment

def thething(string):
	if len(string) != 0:
		query = tweets.Query(string)
		tweets.search_tweets(query,100)
		sentiment.nltk_vader(query)
		return str(query.avg_rate)
	else:
		return 'Need query'
