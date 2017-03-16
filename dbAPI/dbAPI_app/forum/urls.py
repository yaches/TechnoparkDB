from django.conf.urls import url, include

from dbAPI_app.forum.views import create, details

urlpatterns = [
    url(r'^create', create, name = 'create'),
    url(r'^(?P<slug>[\S]+)/details', details, name = 'details')
]