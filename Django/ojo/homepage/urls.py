from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    path('regcon/', views.regcon, name='regcon'),
    path('logcon/', views.logcon, name='logcon'),

    path('login/', views.login, name='login'),
    path('theme/', views.showTheme, name='theme'),
    path('<str:theme>/stay/', views.stayFilter, name='stay'),
    path('detail/', views.stayDetail, name='staydetail'),
]