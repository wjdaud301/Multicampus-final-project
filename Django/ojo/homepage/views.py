# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from homepage.models import User_info
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth


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

        if result is not None:
            # login(result)
            return HttpResponseRedirect(reverse('homepage:theme'))
        else:
            #return render(requests, 'homepage/register.html') 
            return HttpResponseRedirect(reverse('homepage:register'))

def login(requests):
    return render(requests, 'homepage/login.html')

def showTheme(requests):
    return render(requests, 'homepage/theme.html')

def stayFilter(requests):
    return render(requests, 'homepage/stayfilter.html')

def stayDetail(requests):
    return render(requests, 'homepage/staydetail.html')