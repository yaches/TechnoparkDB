from django.conf.urls import url, include

app_name = 'dbAPI_app'
urlpatterns = [
    url(r'^user/', include('dbAPI_app.user.urls')),
    url(r'^forum/', include('dbAPI_app.forum.urls')),
    url(r'^post/', include('dbAPI_app.post.urls')),
    url(r'^thread/', include('dbAPI_app.thread.urls')),
    url(r'^service/', include('dbAPI_app.service.urls'))
]