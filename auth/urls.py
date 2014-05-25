from django.conf.urls import patterns, url
from auth.views import AuthUserView, AuthLoginView

urlpatterns = patterns('',
    url(r'^$', AuthUserView.as_view()),
    url(r'^login/$' , AuthLoginView.as_view()),
)