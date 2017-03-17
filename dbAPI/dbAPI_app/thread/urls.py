from django.conf.urls import url, include

from dbAPI_app.thread.views import *

urlpatterns = [
	url(r'^(?P<id>[0-9]+)/create', id_create, name = 'id_create'),
	url(r'^(?P<slug>[\S]+)/create', slug_create, name = 'slug_create'),
	url(r'^(?P<id>[0-9]+)/vote', id_vote, name = 'id_vote'),
	url(r'^(?P<slug>[\S]+)/vote', slug_vote, name = 'slug_vote'),
	url(r'^(?P<id>[0-9]+)/details', id_details, name = 'id_details'),
	url(r'^(?P<slug>[\S]+)/details', slug_details, name = 'slug_details'),
	url(r'^(?P<id>[0-9]+)/posts', id_posts, name = 'id_posts'),
	url(r'^(?P<slug>[\S]+)/posts', slug_posts, name = 'slug_posts'),
]