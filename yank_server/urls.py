from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^auth/', include('auth.urls')),
    url(r'^entity/', include('entities.urls')),
)
