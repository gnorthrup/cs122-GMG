from django.shortcuts import render

def start(request):
	c = {'name': 'Graham'}
	return render(request, 'little_bird/start.html', c)