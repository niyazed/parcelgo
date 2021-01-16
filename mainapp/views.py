from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Register, Orders
import random

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")



def login(request):
    if request.method == 'POST':
        try:
            data = Register.objects.get(phone = request.POST['phone'])
        except:
            return redirect("/login")
        
        if str(data.phone) == str(request.POST['phone']) and str(data.password) == str(request.POST['password']):
            request.session['name'] = data.name
            request.session['phone'] = data.phone
            request.session['usertype'] = data.usertype
            print(data.name)

            if str(data.usertype) == 'Customer':
                return redirect("/cdash", {"username": request.session['name']})
            else:
                return render("/ddash", {"username": request.session['name']})
        else:
            return redirect("/login")    
    else:
        return render(request, "login.html")




def logout(request):
    request.session.flush()
    return redirect("/login")



def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone'].replace(" ","")
        password1 = request.POST['password1'].replace(" ","")
        password2 = request.POST['password2'].replace(" ","")
        usertype = request.POST['usertype'].replace(" ","")
        email = request.POST['email'].replace(" ","")
        address = request.POST['address']

        register = Register()

        if str(password1) == str(password2):
            register.name = name
            register.phone = phone
            register.password = password1
            register.usertype = usertype
            register.email = email
            register.address = address
            register.save()

            return redirect("/login")
        else:
            return redirect("/signup")


    return render(request, "signup.html")

def ddash(request):
    return render(request, "ddash.html")



def cdash(request):
    if request.method == 'POST' and 'cost_cal' in request.POST:
        height = request.POST['height'].replace(" ","")
        width = request.POST['width'].replace(" ","")
        length = request.POST['length'].replace(" ","")
        weight = request.POST['weight'].replace(" ","")
        base_price = 30

        total_price = int(height) * int(width) * int(length) * int(weight) * base_price

        request.session['height'] = height
        request.session['width'] = width
        request.session['length'] = length
        request.session['weight'] = weight
        request.session['total_price'] = total_price

        return render(request, "cdash.html", {"total_price": total_price})

    elif request.method == 'POST' and 'confirm' in request.POST:
        # rcvr_name = request.POST['rcvr_name']
        # rcvr_email = request.POST['rcvr_email']
        # rcvr_phone = request.POST['rcvr_phone']
        
        # pickup_address = request.POST['pickup_address']
        # deliver_address = request.POST['deliver_address']

        order_id = "ORD-N"+str(random.randint(0,9))+str(random.randint(0,9))
        orders = Orders()
        orders.order_id = order_id
        orders.parcel_height = request.session['height']
        orders.parcel_width = request.session['width']
        orders.parcel_length = request.session['length']
        orders.parcel_weight = request.session['weight']
        orders.total_price = request.session['total_price']

        orders.sender_name = request.session['name']
        orders.sender_phone = request.session['phone']

        orders.receiver_name = request.POST['rcvr_name']
        orders.receiver_phone = request.POST['rcvr_phone']

        orders.pickup_address = request.POST['pickup_address']
        orders.deliver_address = request.POST['deliver_address']
        orders.order_status = "placed"

        orders.save()

        return redirect("/ongoing-order")
        

    else:
        order = Orders.objects.get(sender_phone = request.session['phone'])
        if order.order_status == 'placed':
            return render(request, "cdash.html", {"already": 'You have already an ongoing order!'})
        else:
            return render(request, "cdash.html")



def ongoing_order(request):
    orders = Orders.objects.get(sender_phone = request.session['phone'])
    
    context = {
        "height": orders.parcel_height,
        "width": orders.parcel_width,
        "length": orders.parcel_length,
        "weight": orders.parcel_weight,
        "total_price": orders.total_price,

        "rcvr_name": orders.receiver_name,
        "rcvr_phone": orders.receiver_phone,

        "pickup_address": orders.pickup_address,
        "deliver_address": orders.deliver_address,

        "delman_name": orders.delman_name,
        "delman_phone": orders.delman_phone
    }
    return render(request, "ongoing-order.html", context)



def order_history(request):
    return render(request, "order-history.html")