import json
import os
import time
from datetime import datetime

from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import re_path
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.views.generic import RedirectView

from LottoWebCore.forms import TicketForm, StudentDirectoryForm, UniversityForm, RaffleForm, CityForm, TicketEditForm, \
    SignUpForm
from LottoWebCore.models import Ticket, MiddleMan, Raffle, StudentDirectory, University, City, RegistrationRequest

t_objs = Ticket.objects

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),
]


def index(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    # PageView.objects.create(hostname=hostname)
    return render(request, 'index.html', {
        'hostname': hostname,
        # 'count': PageView.objects.count(),
        'users': Ticket.objects.count()
        # 'user_ratio': (Users.objects.count() / sum([s['self.followers'] for s in Store.objects.filter(
        #    ~Q(collection=django.utils.timezone.datetime(2016, 1, 1, tzinfo=pytz.UTC))
        # ).values('self.followers')])) * 100
    })


@login_required
def lottery(request):
    return render(request, 'dashboard/lottery.html', {
    })


def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(json.dumps(request.POST))
            if not data:
                data = json.loads(request.body.decode("utf-8"))
        except:
            return HttpResponse(json.dumps(None), content_type="application/json")
        if data['model'] == 'REG':
            obj_reg = RegistrationRequest(
                name=data['name'],
                phone=data['phone'],
                email=data['email'],
                raffle=Raffle.objects.get(id=data['raffle']),
                directory=StudentDirectory.objects.get(pk=data['directory'])
            )
            obj_reg.save()
            return redirect('/')
    return render(request, 'dashboard/signup.html', {
        'form': SignUpForm
    })


@login_required
def UserProfile(request):
    return render(request, "account/profile.html", {'META': request.META})


@login_required
def DashBoard(request):
    if request.method == 'POST':
        api_handler(request)
    print(request.user)
    return render(request, "dashboard/dashboard.html",
                  {'META': request.META,
                   'TForm': TicketForm,
                   'TEForm': TicketEditForm,
                   'SDForm': StudentDirectoryForm,
                   'UForm': UniversityForm,
                   'CForm': CityForm,
                   'RForm': RaffleForm})


# https://github.com/django-tastypie/django-tastypie
@login_required
@csrf_protect
def api_handler(request, method=None, data=None):
    # TODO ADD OWNERSHIP RESCTRICTION USER CAN ONLY SEE ITS STORES AND ALLOW STAFF OR SUPER USERS
    # http://stackoverflow.com/questions/12812716/how-do-i-pass-variables-in-django-through-the-url
    # http://www.earthchildpendants.co.uk/gods.html
    data = request.POST.copy()
    #
    print(data)
    lh_user = request.user.username
    #
    response = {'user': lh_user, 'tickets': data}
    #
    if request.method == 'POST':
        try:
            data = json.loads(json.dumps(request.POST))
            if not data:
                data = json.loads(request.body.decode("utf-8"))
        except:
            return HttpResponse(json.dumps(response), content_type="application/json")
        #
        o_data = {'status': 200, 'code': 666, 'msg': 'Ops, your post could not be scheduled. \n Check your stats page '
                                                     'to check if you still have available slots. '}
        #
        if data['method'] == 'ADD':
            if data['model'] == 'TCK':
                try:
                    tickets = []
                    for _ in range(int(data['TCKN'])):
                        tickets.append(Ticket(
                            seller=MiddleMan.objects.get(id=data['Vendedor']),
                            raffle=Raffle.objects.get(id=data['raffle']),
                            directory=StudentDirectory.objects.get(pk=data['directory'])
                        ))
                        time.sleep(0.1)
                    ticket_book = Ticket.objects.bulk_create(tickets)
                    o_data = {'status': 200, 'code': 200, 'msg': 'Your post was scheduled successfully.'}
                except Exception as E:
                    o_data['hadException'] = True
                finally:
                    return HttpResponse(json.dumps(o_data), content_type="application/json")
            elif data['model'] == 'UNI':
                obj_uni = University(name=data['name'], page=data['page'])
                obj_uni.save()
            elif data['model'] == 'CTY':
                obj_cty = City(name=data['name'])
                obj_cty.save()
            elif data['model'] == 'RAF':
                obj_raf = Raffle(
                    name=data['name'],
                    phone=data['phone'],
                    email=data['email'],
                    lottery=datetime.strptime(data['lottery'], "%d/%m/%Y").date(),
                    directory=StudentDirectory.objects.get(pk=data['directory']),
                )
                obj_raf.save()
            elif data['model'] == 'DIR':
                obj_dir = StudentDirectory(
                    name=data['name'],
                    phone=data['phone'],
                    email=data['email'],
                    room=data['room'],
                    city=City.objects.get(pk=data['city']),
                    university=University.objects.get(pk=data['university'])
                )
                obj_dir.save()
        elif data['method'] == 'DEL':
            response = None
            # response = mark_safe(json.dumps({p['fields']['picture']: p['fields'] for p in json.loads(serialize(
            # 'json', None))}))
            return HttpResponse(json.dumps(response), content_type="application/json")
        elif data['method'] == 'request':
            # TODO statistics
            pass
    elif not method:
        response['analytics'] = "method_1"
    elif method == 'following':
        response[method] = "method_2"
    elif method == 'post':
        response[method] = "method_3"
    elif method == 'raffles':
        response[method] = "method_4"
    elif method == 'graph':
        response = "method_5"
    elif method == 'update':
        response['msg'] = "method_6"
    #
    return HttpResponse(json.dumps(response), content_type="application/json")


class SellerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return MiddleMan.objects.none()
        #
        qs = MiddleMan.objects.all()
        #
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        #
        return qs


class RaffleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Raffle.objects.none()
        #
        qs = Raffle.objects.all()
        #
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        #
        return qs


class StudentDirectoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return StudentDirectory.objects.none()
        #
        qs = StudentDirectory.objects.all()
        #
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        #
        return qs


class TicketAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Ticket.objects.none()
        #
        if self.request.user.is_superuser:
            qs = Ticket.objects.all()
        else:
            qs = Ticket.objects.filter(directory=MiddleMan.objects.get(user=self.request.user).directory,
                                       activated=False)
        #
        if self.q:
            qs = qs.filter(id__istartswith=self.q)
        #
        return qs
