import random
import string
import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import ReservationForm

from requests_oauthlib import OAuth2Session
import environ
import base64
import webbrowser

env = environ.Env()

SECRET_KEY = env("PAYMONGO_SECRET_KEY")
HOST_URL = env("HOST_URL")
MICROSOFT_CLIENT_SECRET = env("MICROSOFT_CLIENT_SECRET")
MICROSOFT_CLIENT_ID = env("MICROSOFT_CLIENT_ID")


User = get_user_model()
def initialize_oauth():
    client_id = MICROSOFT_CLIENT_ID
    scope = ["User.Read", "profile", "email", "openid"]
    redirect_uri = HOST_URL+'callback'

    return OAuth2Session(client_id,scope=scope,redirect_uri=redirect_uri)

def login(request):
    authorization_base_url = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize'

    oauth = initialize_oauth()
    authorization_url, state = oauth.authorization_url(authorization_base_url)

    # return HttpResponse('Please go here and authorize ' + authorization_url )
    context = {"authorization_url": authorization_url }
    return render(request, "forms/login_redirect.html", context)

def callback(request):
    client_secret = MICROSOFT_CLIENT_SECRET
    token_url = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/token'
    code = request.GET.get('code','')
    oauth = initialize_oauth()
    token = oauth.fetch_token(token_url, client_secret=client_secret, code=code)

    req = requests.get("https://graph.microsoft.com/v1.0/me?$select=displayName,givenName,jobTitle,mail,department,id", headers={"Authorization": "Bearer " + token["access_token"]})
    response = req.json()

    try:
        user = User.objects.get(email=response["mail"])
    except User.DoesNotExist:
        email = response["mail"]
        if email.split('@')[1] == "cclcentrex.edu.ph":
            random_password = "".join(random.choice(string.ascii_letters) for i in range(32))
            user = User(username=response["mail"], email=response["mail"], password=make_password(random_password))
            user.save()
            Profile.objects.create(
                user=user,
                name=response.get("displayName"),
                role=response.get("jobTitle"),
                department=response.get("department")
            )
        else:
            return HttpResponseRedirect('/login')
    auth_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return HttpResponseRedirect('/')

@csrf_exempt
def webhooks(request):
    req_json = json.loads(request.body.decode("utf-8"))["data"]["attributes"]
    print(req_json["type"])
    if req_json["type"] == "checkout_session.payment.paid":
        if req_json["data"]["attributes"]["metadata"]["type"] == "order":
            order_id = req_json["data"]["attributes"]["metadata"]["id"]

            order = Order.objects.get(id=order_id)
            print(order)
            order.paid = True
            order.save()
        elif req_json["data"]["attributes"]["metadata"]["type"] == "reservation":
            reservation_id = req_json["data"]["attributes"]["metadata"]["id"]
            reservation = Order.objects.get(id=reservation_id)
            reservation.paid = True
            reservation.save()
            order = reservation.order
            reservations = order.reservations.all()
            all_paid = True
            for reservation in reservations:
                if not reservation.paid:
                    all_paid = False
                    break
            if all_paid:
                order.paid = True
                order.save()


    return HttpResponse(200)

def source_callback(request):
    print("test")

@login_required(login_url='/login')
def index(request):
    if not hasattr(request.user,"profile"):
        return redirect('login')
    profile = request.user.profile
    active_lunch_form = LunchForm.objects.filter(active=True).first()
    active_snacks_form = SnacksForm.objects.filter(active=True).first()

    if not active_lunch_form:
        context = {
            "profile" : profile,
            "orders": profile.order_set.all(),
            "submitted": len(profile.order_set.filter(form=active_lunch_form)) != 0
        }
        return render(request, "forms/index.html", context)

    if request.method == "POST":
        total_paid = 0

        form_type = request.POST.getlist("form")[0]
        if form_type == "lunch_form":
            order = Order.objects.create(form=active_lunch_form, profile=profile)
        elif form_type == "snacks_form":
            order = Order.objects.create(form=active_snacks_form, profile=profile)
        weekdays = ["monday","tuesday","wednesday","thursday","friday"]
        food_items_dict = {"1": [], "2": [], "3": [], "4": [], "5": []}
        for key,value in request.POST.dict().items():

            if "quantity" in key and int(value) != 0:
                food_item_id, weekday_num, *rest = key.split("-")
                food_items_dict[weekday_num].append({"food_item_id": food_item_id, "quantity": value})

        for key, value in food_items_dict.items():
            reservation = Reservation.objects.create(weekday=str(key))
            for food_item_entry in value:
                print(food_item_entry)
                food_item = FoodItem.objects.get(id=food_item_entry["food_item_id"])
                total_paid += food_item.price * int(food_item_entry["quantity"])
                selection = Selection.objects.create(reservation=reservation, food_item=food_item, quantity=food_item_entry["quantity"])

                selection.save()


            order.reservations.add(reservation)
        order.total_paid = total_paid
        order.save()


        return redirect('index')

    lunch_options = active_lunch_form.options.all().order_by("weekday")

    snacks_options = active_snacks_form.options.all().order_by("weekday")

    context = {
        "active_lunch_form": active_lunch_form,
        "active_snacks_form": active_snacks_form,
        "lunch_options": lunch_options,
        "snacks_options": snacks_options,
        "submitted_lunch": len(profile.order_set.filter(form=active_lunch_form)) != 0,
        "submitted_snacks": len(profile.order_set.filter(form=active_snacks_form)) != 0,
        "profile" : profile,
        "orders": reversed(profile.order_set.all()),

    }
    if request.user_agent.is_mobile:
        print("ay")
        return render(request, "forms/mobile_index.html", context)
    return render(request, "forms/index.html", context)

@csrf_exempt
def delete_order(request,id):
    if request.method == "POST":
        order = Order.objects.get(id=id)
        if order.paid is False:
            order.delete()
        return redirect('index')

@csrf_exempt
def pay_order(request,id):
    secret_key = "sk_test_fdM4unQJZYQqQWvQN1xyHMG7".encode("ascii")

    base64_secret_key = base64.b64encode(secret_key).decode("ascii")
    headers = {
        "accept": "application/json",
        "authorization": "Basic "+base64_secret_key,
        "content-type": "application/json"
    }

    cs_url = "https://api.paymongo.com/v1/checkout_sessions"
    pay_type = request.POST["pay_type"]
    if pay_type == "order":
        order = Order.objects.get(id=id)

        cs_payload = { "data": { "attributes": {
                    "payment_method_types": ["gcash"],
                    "line_items": [
                        {
                            "amount": order.total_paid*100,
                            "currency": "PHP",
                            "name": "Total",
                            "quantity": 1
                        },
                        {
                            "amount": round((order.total_paid*100)*0.025),
                            "currency": "PHP",
                            "name": "Small Service Fee",
                            "quantity": 1
                        }
                    ],
                    "description": "test",
                    "send_email_receipt": False,
                    "show_description": True,
                    "show_line_items": True,
                    "success_url": HOST_URL,

                    "metadata": {
                        "type": "order",
                        "id": id
                    }
                } } }
    elif pay_type == "reservation":
        reservation = Reservation.objects.get(id=id)
        total_paid = 0
        food_items = reservation.food_items
        for food in food_items.values():
            total_paid += food["price"]
        cs_payload = { "data": { "attributes": {
                    "payment_method_types": ["gcash"],
                    "line_items": [
                        {
                            "amount": total_paid*100,
                            "currency": "PHP",
                            "name": "Total",
                            "quantity": 1
                        },
                        {
                            "amount": round((total_paid*100)*0.025),
                            "currency": "PHP",
                            "name": "Small Service Fee",
                            "quantity": 1
                        }
                    ],
                    "description": "test",
                    "send_email_receipt": False,
                    "show_description": True,
                    "show_line_items": True,
                    "success_url": HOST_URL,

                    "metadata": {
                        "type": "reservation",
                        "id": id
                    }
                } } }
    cs_response = requests.post(cs_url, json=cs_payload, headers=headers)
    print(cs_response.json())
    checkout_url = cs_response.json()["data"]["attributes"]["checkout_url"]
    # webbrowser.open(checkout_url)

    return HttpResponse(checkout_url)


def print_form(request, id):
    if request.user.is_superuser:
        weekdays = Option.WEEKDAYS
        form = Form.objects.get(id=id)
        orders = Order.objects.filter(form=form)

        display = {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": []
        }
        for order in orders:
            reservations = order.reservations.all()
            for reservation in reservations:

                display[weekdays[int(reservation.weekday)-1][1]].append(reservation)


        context = {
            "weekdays": ["monday","tuesday","wednesday","thursday","friday"],
            "form": form,
            "orders": orders,
            "display": display,

        }
        return render(request, "admin/print_form.html", context)
    else:
        return redirect('index')

def check_quantities(request, id):
    if request.user.is_superuser:
        weekdays = Option.WEEKDAYS
        form = Form.objects.get(id=id)
        orders = Order.objects.filter(form=form)



        count = {
            "monday": {},
            "tuesday": {},
            "wednesday": {},
            "thursday": {},
            "friday": {},
            "total": {}
        }

        for option in form.options.all():
            for food_item in option.food_items.all():
                count[weekdays[int(option.weekday)-1][1]][food_item.name] = 0
                if food_item.name not in count["total"]:
                    count["total"][food_item.name] = 0

        for order in orders:
            reservations = order.reservations.all()
            for reservation in reservations:
                for selection in reservation.selection_set.all():
                    count[weekdays[int(reservation.weekday)-1][1]][selection.food_item.name] += selection.quantity
                    count["total"][selection.food_item.name] += selection.quantity

        context = {
            "count": count,
        }
        return render(request, "admin/check_quantities.html", context)
    else:
        return redirect('index')

def check_order(request, id):
    if request.user.is_superuser:
        weekdays = Option.WEEKDAYS
        order = Order.objects.get(id=id)

        display = {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": []
        }

        reservations = order.reservations.all()
        for reservation in reservations:
            display[weekdays[int(reservation.weekday)-1][1]].append(reservation)


        context = {
            "weekdays": ["monday","tuesday","wednesday","thursday","friday"],

            "display": display,

        }
        return render(request, "admin/check_order.html", context)
    else:
        return redirect('index')