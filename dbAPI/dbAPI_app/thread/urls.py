from django.conf.urls import url, include

from dbAPI_app.thread.views import id_create, slug_create

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/create', id_create, name = 'id_create'),
    url(r'^(?P<slug>[\S]+)/create', slug_create, name = 'slug_create'),
    # url(r'^(?P<slug>[\S]+)/details', details, name = 'details'),
    # url(r'^(?P<slug>[\S]+)/threads', get_threads, name = 'get_threads')
]