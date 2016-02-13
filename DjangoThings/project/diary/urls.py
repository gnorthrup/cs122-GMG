from django.conf.urls import url
from django.contrib import admin

from django.http import HttpResponse

from . import views

urlpatterns = [
	url(r'', views.start),
	url(r'^about/$', views.about)]