from django.conf.urls import url, include

from dbAPI_app.user.views import create, profile

urlpatterns = [
    url(r'^(?P<nickname>[\S]+)/create', create, name = 'create'),
    url(r'^(?P<nickname>[\S]+)/profile', profile, name = 'profile')
]