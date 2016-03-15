from django.conf.urls import url
from django.contrib import admin

from django.http import HttpResponse

from . import views

#Modified: The url dispatcher is a Django file
#but we added our links to the patterns

urlpatterns = [
	url(r'^about/$', views.about, name='about'),
	url(r'^ack/$', views.ack, name='ack'),
	url(r'', views.start, name='search'),]
