<<<<<<< HEAD
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
    path('<str:name>detail/', views.stayDetail, name='staydetail'),
=======
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    path('regcon/', views.regcon, name='regcon'),
    path('logcon/', views.logcon, name='logcon'),
    path('choice/', views.choice, name ='choice'),
    path('totalstay/', views.totalstay, name ='totalstay'),
    path('find/', views.find, name ='find'),
    path('popular/', views.popular, name ='popular'),    

    path('login/', views.login, name='login'),
    path('theme/', views.showTheme, name='theme'),
    path('<str:theme>/stay/', views.stayFilter, name='stay'),
    path('<str:name>/detail/', views.stayDetail, name='staydetail'),
>>>>>>> 26f4beea27c7167f6d41785eb695130952d1665e
]