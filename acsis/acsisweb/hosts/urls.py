"""
    hosts.urls
"""
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.hosts_index),
    url(r'^api/$', views.host_list),
]


