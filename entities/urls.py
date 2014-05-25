from django.conf.urls import patterns, url
from entities import views

from entities.views import EntityNoteCompoundPostView, EntityView, \
    EntityNoteView 

urlpatterns = patterns('',
    url(r'^$', EntityView.as_view()),
    url(r'^(?P<radius>[0-9]{2})/$', 'entities.views.list_entities_inside_radius'),
    # url(r'^note/$', 'entities.views.list_notes'),
    url(r'^note/(?P<eid>[0-9]+)/$', 'entities.views.list_notes'),
    url(r'^compound/$', EntityNoteCompoundPostView.as_view()),

    # Get entities within a radius
    url(r'^radius/(?P<arg_lat>[0-9]\.[0-9]+)/(?P<arg_lng>[0-9]\.[0-9]+)/(?P<radius>[0-9]+)/$',
        'entities.views.list_entities_inside_radius'),
)