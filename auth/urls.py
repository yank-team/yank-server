from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$'       , 'auth.views.list_user'),
    url(r'^login/$' , 'auth.views.authenticate'),
    url(r'^logout/$', 'auth.views.logout'),
    url(r'^verify/$', 'auth.views.verify_apik'),
)