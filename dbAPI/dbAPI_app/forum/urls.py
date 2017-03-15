from django.conf.urls import url, include

from dbAPI_app.forum.views import create

urlpatterns = [
    url(r'^/create', create, name = 'create')
    # url(r'^(?P<nickname>[\S]+)/profile', profile, name = 'profile')
]