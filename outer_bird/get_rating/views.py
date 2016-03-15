from django.shortcuts import render
from django.http import HttpResponse
from get_rating.doesthething import thething

#Modified: views.py is a Django file, but it is
#blank upon creation. we populated it with the code
#to produce the html files

def start(request):
	if request.method == 'GET':
		string = request.GET.get('query', '')
		category = request.GET.get('category', '')
		top = request.GET.get('top_10', '')
		bottom = request.GET.get('bottom_10', '')
		newstring, best, worst, top_tweets, bottom_tweets = thething(string, category, top, bottom)
		c = {'return':newstring, 'best':best, 'worst':worst, 'query':string,
			'top_tweets':top_tweets, 'bottom_tweets':bottom_tweets}
		return render(request, 'get_rating/start.html', c)
	else:
		c = {'name': 'Graham'}
		return render(request, 'get_rating/start.html', c)

def about(request):
	c = {}
	return render(request, 'get_rating/about.html', c)

def ack(request):
	c = {}
	return render(request, 'get_rating/ack.html', c)
