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
            return render(request, "login.html", {"invalid_cred": 'Invalid Credentials'}) 
        
        if str(data.password) == str(request.POST['password']):
            request.session['name'] = data.name
            request.session['phone'] = data.phone
            print(request.session['phone'])
            request.session['usertype'] = data.usertype
            print(data.name)

            if str(data.usertype) == 'Customer':
                return redirect("/cdash", {"username": request.session['name']})
            else:
                return redirect("/ddash", {"username": request.session['name']})
        else:
            # return redirect("/login")
            return render(request, "login.html", {"invalid_cred": 'Invalid Credentials'})    
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
    try:
        order = Orders.objects.get(delman_phone = request.session['phone'])
        if order.order_status == 'picked':
            return render(request, "ddash.html", {"picked": 'You have already picked an order!'})
        else:
            orders = Orders.objects.filter(order_status = 'placed')
            return render(request, "ddash.html", {"orders": orders})
    except:
        orders = Orders.objects.filter(order_status = 'placed')
        return render(request, "ddash.html", {"orders": orders})
        # return render(request, "ddash.html")



def delivered(request):
    if request.method == 'POST':
        order = Orders.objects.get(delman_phone = request.session['phone'], order_status = 'picked')
        order.order_status = 'delivered'
        order.save()
        return render(request, "ddash.html", {"delivered": 'Order delivered Successfully!'})



def cdash(request):
    if request.method == 'POST' and 'cost_cal' in request.POST:
        height = request.POST['height'].replace(" ","")
        width = request.POST['width'].replace(" ","")
        length = request.POST['length'].replace(" ","")
        weight = request.POST['weight'].replace(" ","")
        distance = request.POST['distance'].replace(" ","")
        base_price = 5

        total_price = int(height) + int(width) + int(length) + int(weight) + base_price * int(distance)

        request.session['height'] = height
        request.session['width'] = width
        request.session['length'] = length
        request.session['weight'] = weight
        request.session['distance'] = distance
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
        # orders.distance = request.session['distance']
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
        try:
            order = Orders.objects.filter(sender_phone = request.session['phone']).order_by('id').last()
            print(order)
            if order.order_status == 'placed' or order.order_status == 'picked':
                return render(request, "cdash.html", {"already": 'You have already an ongoing order!'})
            else:
                return render(request, "cdash.html") 
        except:
            return render(request, "cdash.html")




def ongoing_order(request):
    try:
        orders = Orders.objects.get(sender_phone = request.session['phone'], order_status = 'placed')
        
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
    except:
        try:
            orders = Orders.objects.get(sender_phone = request.session['phone'], order_status = 'picked')
            
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
        except:
            return render(request, "ongoing-order.html")
        



def picked_order(request):
    if request.method == 'POST':
        ord_id = request.POST['pickup-btn']
        orders = Orders.objects.get(order_id = ord_id)
        orders.delman_name = request.session['name']
        orders.delman_phone = request.session['phone']
        orders.order_status = "picked"
        orders.save()

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
    else:
        try:
            orders = Orders.objects.get(delman_phone = request.session['phone'], order_status = 'picked')
        except:
            return render(request, "picked-order.html")
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
        # return render(request, "picked-order.html", context)
    return render(request, "picked-order.html", context)

def payment(request):
    return render(request, "payment.html")


def order_history(request):
    orders = Orders.objects.filter(order_status = 'delivered', sender_phone = request.session['phone'])
    return render(request, "order-history.html", {"orders": orders})