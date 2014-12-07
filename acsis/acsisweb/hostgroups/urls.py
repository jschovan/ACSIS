"""
    hosts.urls
"""
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.hostgroups_index),
    url(r'^api/$', views.hostgroup_list),
]


