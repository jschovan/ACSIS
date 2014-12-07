"""
    hosts.urls
"""
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.services_index),
    url(r'^api/$', views.service_list),
]


