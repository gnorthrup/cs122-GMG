from django.shortcuts import render
from django.http import HttpResponse
from get_rating.doesthething import thething

def start(request):
	if request.method == 'GET':
		string = request.GET.get('query', '')
		category = request.GET.get('category', '')
		top = request.GET.get('top_10', '')
		bottom = request.GET.get('bottom_10', '')
		newstring, best, worst, plt = thething(string, category, top, bottom)
		c = {'return':newstring, 'best':best, 'worst':worst, 'plot':plt, 'query':string}
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
