from django.conf.urls import url, include

# from . import views
from dbAPI_app.user.views import create

urlpatterns = [
    url(r'^(?P<nickname>[\S]+)/create', create, name = 'create'),
    # url(r'^(?P<nickname>)/profile/', views.profile, name = profile)
]