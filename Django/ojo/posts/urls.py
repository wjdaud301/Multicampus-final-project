from django.conf.urls import url, include
from . import views

appname='posts'

urlpatterns = [
    url(r'', views.index),
]


