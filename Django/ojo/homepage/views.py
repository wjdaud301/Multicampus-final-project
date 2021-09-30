# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from homepage.models import User_info
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth

# from homepage.MongoDbManager import MongoDbManager
from datetime import datetime
import pandas as pd
from homepage.Api import Json
#from .forms import SignUpForm


filter = {'one' : '나홀로 여행', 'two':'도심속 휴식', 'three':'정적인 휴식','four':'아이와 함께','five':'시티뷰','six':'한옥','seven':'오션 뷰','eight':'숲 속'}
# Create your views here.
def home(requests):
    return render(requests, 'homepage/index.html')

def register(requests):
    return render(requests, 'homepage/register.html')

def regcon(requests):
    userid = requests.POST['userid']
    email = requests.POST['emailid']
    passwd = requests.POST['userpw']

    qs = User.objects.create_user(userid, email, passwd)
    qs.save()

    return HttpResponseRedirect(reverse('homepage:register'))

def logcon(requests):
    if requests.method == 'POST':
        userid = requests.POST['userid']
        passwd = requests.POST['userpw']
        result = authenticate(username = userid, password = passwd)
        user=User()


        if result is not None:
            # login(result)
            return HttpResponseRedirect(reverse('homepage:theme'))
        else:
            #return HttpResponseRedirect(reverse('homepage:relogin'))
            return render(requests, 'homepage/relogin.html')
            

def login(requests):
    return render(requests, 'homepage/login.html')

def showTheme(requests):
    context = filter
    return render(requests, 'homepage/theme.html', context)

def stayFilter(requests, theme):
    print(theme)
    nowtime = datetime.today().strftime("%Y-%m-%d")
    co_if = Json.corona_info(nowtime)
    insta_if = Json.insta_info(theme)
    co_if.update(insta_if)
    co_if['filter'] = theme
    print(co_if)
    return render(requests, 'homepage/stayfilter.html', co_if)

def stayDetail(requests):
    return render(requests, 'homepage/staydetail.html')

