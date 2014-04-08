from django.conf.urls import patterns, include, url
from yank_entities.views import EntityLocation

urlpatterns = patterns('',
    url(r'location/$', EntityLocation.as_view()),
)
