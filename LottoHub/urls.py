"""LottoHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from LottoWebCore.views import index, lottery, UserProfile, DashBoard, signup, SellerAutocomplete, \
    RaffleAutocomplete, StudentDirectoryAutocomplete, api_handler

app_name = 'LottoHub'

urlpatterns = [
    url(r'^$', index, name='index'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls, name='admin'),
    url(r'^sorteio/', lottery, name='sorteio'),
    path('profile/', UserProfile, name='profile'),
    path('dashboard/', DashBoard, name='dashboard'),
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^profile/', UserProfile, name='profile'),
    url(r'^api/', api_handler, name='api'),
    url(r'^seller-autocomplete/$', SellerAutocomplete.as_view(), name='seller-autocomplete'),
    url(r'^raffle-autocomplete/$', RaffleAutocomplete.as_view(), name='raffle-autocomplete'),
    url(r'^ticket-autocomplete/$', StudentDirectoryAutocomplete.as_view(), name='ticket-autocomplete'),
    url(r'^directory-autocomplete/$', StudentDirectoryAutocomplete.as_view(), name='directory-autocomplete')
]
