from django.conf.urls import url, include

from dbAPI_app.service.views import *

urlpatterns = [
    url(r'^status', status, name = 'status'),
    url(r'^clear', clear, name = 'clear'),
]