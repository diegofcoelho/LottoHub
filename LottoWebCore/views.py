import io
import json
import math
import os
import time
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from dal import autocomplete
from django.contrib.auth.decorators import login_required
# from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import re_path
# from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.views.generic import RedirectView

from LottoHub.settings import BASE_DIR
from LottoWebCore.forms import SignUpForm, TicketEditForm
from LottoWebCore.forms import TicketForm, StudentDirectoryForm, UniversityForm, RaffleForm, CityForm, \
    TicketActivationForm
from LottoWebCore.methods import sendMail
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
        'bilhetes': Ticket.objects.count()
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
    return render(request, "dashboard/dashboard.html",
                  {'META': request.META,
                   'TForm': TicketForm,
                   'ActivationForm': TicketActivationForm,
                   'EditForm': TicketEditForm,
                   'SDForm': StudentDirectoryForm,
                   'UForm': UniversityForm,
                   'CForm': CityForm,
                   'RForm': RaffleForm})


# https://github.com/django-tastypie/django-tastypie
@login_required
@csrf_protect
def api_handler(request, method=None):
    # TODO ADD OWNERSHIP RESCTRICTION USER CAN ONLY SEE ITS STORES AND ALLOW STAFF OR SUPER USERS
    # http://stackoverflow.com/questions/12812716/how-do-i-pass-variables-in-django-through-the-url
    # http://www.earthchildpendants.co.uk/gods.html
    #
    response = None
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
        print(data)
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
                        time.sleep(0.001)
                        print(1)
                    ticket_ids = [t.id for t in tickets]
                    #
                    request.session['tickets_id'] = json.dumps(ticket_ids)
                    #
                    Ticket.objects.bulk_create(tickets)
                except Exception as E:
                    print(E)
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
        elif data['method'] == 'EDT':
            if data['model'] == 'TCK_A':
                try:
                    ticket = Ticket.objects.get(id=data['id'])
                    ticket.name = data['name']
                    ticket.phone = data['phone']
                    ticket.email = data['email']
                    ticket.save()
                    #
                    if 'DYNO' in os.environ:
                        data = {'ticket_id': ticket.id,
                                'raffle': ticket.raffle,
                                'name': ticket.name,
                                'phone': ticket.phone,
                                'email': ticket.email,
                                'seller': ticket.seller,
                                'seller_email': ticket.seller.email,
                                'prizes': ticket.raffle.prizes
                                }
                        #
                        sendMail('ATV', data)
                        #
                        ticket.notified = True
                        ticket.activated = True
                        ticket.save()
                    #
                except Exception as E:
                    print(E)
            if data['model'] == 'TCK_E':
                try:
                    ticket = Ticket.objects.get(id=data['id'])
                    ticket.name = data['name']
                    ticket.phone = data['phone']
                    ticket.email = data['email']
                    ticket.save()
                except Exception as E:
                    print(E)
        elif data['method'] == 'ATV':
            if data['model'] == 'TCK_A':
                try:
                    ticket = Ticket.objects.get(id=data['id'])
                    ticket.name = data['name']
                    ticket.phone = data['phone']
                    ticket.email = data['email']
                    ticket.save()
                    #
                    if 'DYNO' in os.environ:
                        data = {'ticket_id': ticket.id,
                                'raffle': ticket.raffle,
                                'name': ticket.name,
                                'phone': ticket.phone,
                                'email': ticket.email,
                                'seller': ticket.seller,
                                'seller_email': ticket.seller.email,
                                'prizes': ticket.raffle.prizes
                                }
                        #
                        sendMail('ATV', data)
                        #
                        ticket.notified = True
                        ticket.activated = True
                        ticket.save()
                    #
                except Exception as E:
                    print(E)
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
            ticket_status = self.forwarded.get('ticket_status', None)
            qs = Ticket.objects.filter(directory=MiddleMan.objects.get(user=self.request.user).directory,
                                       activated=ticket_status)
        #
        if self.q:
            qs = qs.filter(id__istartswith=self.q)
        #
        return qs


@login_required
@csrf_protect
def pdf_gen(request):
    #
    if request.session.get('tickets_id') is None:
        return redirect('/dashboard')
    #
    codes = json.loads(request.session.get('tickets_id'))
    request.session['tickets_id'] = None
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Opens an image
    bg = Image.open(os.path.abspath(BASE_DIR + "//staticfiles//images//ticket.png"))
    # The width and height of the background tile
    bg_w, bg_h = bg.size
    #
    ticket_number = len(codes)
    #
    # codes_blank = math.ceil(ticket_number / 6) * 6 - ticket_number
    # codes.extend(['' for _ in range(0, codes_blank)])
    #
    # ticket_number = len(codes)
    ticket_pages = math.ceil(ticket_number / 12)
    #
    # ticket_number = 7
    tickets_page_series = [12 for i in range(0, ticket_number, 12)]
    tickets_page_series.pop(0) if ticket_number % 12 > 0 else []
    tickets_page_series.extend([ticket_number % 12] if ticket_number % 12 > 0 else [])
    font_path = os.path.abspath(BASE_DIR + '//staticfiles//fonts//Ticketing.ttf')
    #
    fnt_ticket = ImageFont.truetype(font_path, 30)
    fnt_title = ImageFont.truetype(font_path, 45)
    fnt_end = ImageFont.truetype(font_path, 25)
    fnt_date = ImageFont.truetype(font_path, 65)
    fnt_staff = ImageFont.truetype(font_path, 55)
    code_idx = 0
    #
    tickets_total = 0
    #
    for page in range(0, ticket_pages):
        # Creates a new empty image, RGB mode, and size 1240 by ticket_height
        im = Image.new('RGB', (1240, 1754), (255, 255, 255))
        #
        page_lines = math.ceil(tickets_page_series[page] / 6)
        page_columns = math.ceil(tickets_page_series[page] / (tickets_page_series[page] / 6))
        #
        # The width and height of the new image
        # w, h = im.size
        # Iterate through a grid, to place the background tile
        for i in range(0, bg_w * page_columns, bg_w):
            for j in range(0, bg_h * page_lines, bg_h):
                if tickets_total < len(codes):
                    bg = Image.eval(bg, lambda x: x + (i + j) / 1000)
                    im.paste(bg, (i, j))
                    tickets_total += 1
                else:
                    break
        #
        d = ImageDraw.Draw(im)
        for line in range(0, page_lines):
            if code_idx > len(codes) - 1:
                break
            for column in range(0, page_columns):
                if code_idx > len(codes) - 1:
                    break
                d.text((33 + column * bg_w, 160 + line * bg_h), "Organização:", font=fnt_end, fill=(0, 0, 0))
                d.text((45 + column * bg_w, 180 + line * bg_h), "DAEQI", font=fnt_staff, fill=(0, 0, 0))
                d.text((33 + column * bg_w, 230 + line * bg_h), "Sorteio:", font=fnt_end, fill=(0, 0, 0))
                d.text((33 + column * bg_w, 250 + line * bg_h), "21/06", font=fnt_date, fill=(0, 0, 0))
                d.text((35 + column * bg_w, 330 + line * bg_h), "BILHETE", font=fnt_title, fill=(0, 0, 0))
                d.text((35 + column * bg_w, 40 + bg_h / 2 + line * bg_h), "BILHETE", font=fnt_title, fill=(0, 0, 0))
                d.text((35 + column * bg_w, 370 + line * bg_h), codes[code_idx], font=fnt_ticket, fill=(0, 0, 0))
                d.text((35 + column * bg_w, 80 + bg_h / 2 + line * bg_h), codes[code_idx], font=fnt_ticket,
                       fill=(0, 0, 0))
                code_idx += 1
        #
        im.save(buffer, 'pdf')
    buffer.seek(0)

    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline;filename=hello.pdf'
    return response
