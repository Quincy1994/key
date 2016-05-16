from django.conf.urls import patterns, url
from keyproject.views import key

urlpatterns = patterns('',
    url(r'^$', key, name='key'),
    url(r'^key$', key, name='key'),
    )