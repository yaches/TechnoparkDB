from django.conf.urls import url, include

from dbAPI_app.post.views import *

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/details', details, name = 'details'),
]