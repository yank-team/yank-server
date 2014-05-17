from django.conf.urls import patterns, url
from entities import views

urlpatterns = patterns('',
    url(r'^$', 'entities.views.list_entities'),
    url(r'^(?P<radius>[0-9]{2})/$', 'entities.views.list_entities_inside_radius'),
    url(r'^notes/$', 'entities.views.post_entity_note'),
    url(r'^notes/(?P<eid>[0-9]+)/$' , 'entities.views.list_entity_notes'),
)