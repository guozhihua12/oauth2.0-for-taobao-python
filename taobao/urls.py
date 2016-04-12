__author__ = 'apple'
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('taobao.views',
    url('^login/$', 'login', name='taobao_login'),
    url(r'^auth/$', 'auth', name='taobao_auth'),
)