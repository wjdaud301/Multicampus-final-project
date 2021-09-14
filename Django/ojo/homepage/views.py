# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def home(requests):
    return render(requests, 'homepage/index.html')

def login(requests):
    return render(requests, 'homepage/login.html')

def showTheme(requests):
    return render(requests, 'homepage/theme.html')

def stayFilter(requests):
    return render(requests, 'homepage/stayfilter.html')

def stayDetail(requests):
    return render(requests, 'homepage/staydetail.html')