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

from LottoWebCore.views import RaffleAutocomplete, StudentDirectoryAutocomplete, api_handler, pdf_gen, lottery_b, \
    lottery_c, PrizesAC
from LottoWebCore.views import index, lottery, DashBoard, signup, SellerAutocomplete, TicketAutocomplete, ticket_check

app_name = 'LottoHub'

urlpatterns = [
    url(r'^$', index, name='index'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls, name='admin'),
    url(r'^sorteio/', lottery, name='sorteio'),
    url(r'^sorteio2/', lottery_c, name='sorteio2'),
    url(r'^nyx/', lottery_b, name='nyx'),
    url(r'^pdf/', pdf_gen, name='pdf'),
    path('dashboard/', DashBoard, name='dashboard'),
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^api/', api_handler, name='api'),
    path('validar/', ticket_check, name='validar'),
    url(r'^seller-autocomplete/$', SellerAutocomplete.as_view(), name='seller-autocomplete'),
    url(r'^raffle-autocomplete/$', RaffleAutocomplete.as_view(), name='raffle-autocomplete'),
    url(r'^ticket-autocomplete/$', TicketAutocomplete.as_view(), name='ticket-autocomplete'),
    url(r'^prizes-autocomplete/$', PrizesAC.as_view(), name='prizes-autocomplete'),
    url(r'^directory-autocomplete/$', StudentDirectoryAutocomplete.as_view(), name='directory-autocomplete')
]
