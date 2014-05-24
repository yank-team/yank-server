from django.conf.urls import patterns, url
from entities import views

from entities.views import EntityView

urlpatterns = patterns('',
    url(r'^$', EntityView.as_view()),
    url(r'^(?P<radius>[0-9]{2})/$', 'entities.views.list_entities_inside_radius'),
    url(r'^notes/$', 'entities.views.post_entity_note'),
    url(r'^notes/(?P<eid>[0-9]+)/$' , 'entities.views.list_entity_notes'),
)