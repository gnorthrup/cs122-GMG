from django.shortcuts import render

# Create your views here.
def start(request):
	c = {'name': 'Graham',
		'foods': ['Yakisoba', 'Pizza', 'Fried Chicken']
		}
	return render(request, 'diary/start.html', c)