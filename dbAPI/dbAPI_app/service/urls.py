from django.conf.urls import url, include

from dbAPI_app.service.views import *

urlpatterns = [
    url(r'^status', status, name = 'status'),
    url(r'^clear', clear, name = 'clear'),
    url(r'^test', test, name = 'test'),
    # url(r'^pg_stat', pg_stat, name = 'pg_stat'),
    # url(r'^explain', explain, name = 'explain'),
]