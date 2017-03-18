from django.conf.urls import url, include

from dbAPI_app.forum.views import *

urlpatterns = [
    url(r'^create', create, name = 'create'),
    url(r'^(?P<slug>[\S]+)/details', details, name = 'details'),
    url(r'^(?P<slug>[\S]+)/create', create_thread, name = 'create_thread'),
    url(r'^(?P<slug>[\S]+)/threads', get_threads, name = 'get_threads'),
    url(r'^(?P<slug>[\S]+)/users', get_users, name = 'get_users'),
]