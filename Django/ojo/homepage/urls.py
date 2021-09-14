from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('theme/', views.showTheme, name='theme'),
    path('stay/', views.stayFilter, name='stay'),
    path('detail/', views.stayDetail, name='staydetail'),
]