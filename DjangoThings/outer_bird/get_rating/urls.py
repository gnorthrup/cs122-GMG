from django.conf.urls import url
from django.contrib import admin

from django.http import HttpResponse

from . import views

urlpatterns = [
	url(r'^about/$', views.about, name='about'),
	url(r'^ack/$', views.ack, name='ack'),
	url(r'', views.start, name='search'),]
