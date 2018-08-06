from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from device.models import Device,Order,Project,Supplement,Department
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q,F,Count
import datetime

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url = '/device/404')
def updategiveback(request, id):
    order = get_object_or_404(Order, id=id)
    order.device.status = 'Free'
    order.device.save()
    order.orderstatus = 'Completed'
    order.givebackdate = datetime.datetime.today()
    order.save()
    order_list = Order.objects.all().filter(orderstatus = 'Requesting')
    return render(request, 'order/order_list.html',{'order_list' : order_list})

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url = '/device/404')
def listgiveback(request):
    order_list = Order.objects.all().filter(orderstatus = 'Requesting')
    return render(request, 'order/order_list.html',{'order_list' : order_list})

@login_required(login_url="/accounts/login")
def giveback(request, id, username):
    order = get_object_or_404(Order, id=id)
    # order.device.status = 'Free'
    # order.device.save()
    order.orderstatus = 'Requesting'
    #order.givebackdate = datetime.datetime.today()
    order.save()
    order_list = Order.objects.filter(account__username = username )
    return render(request, 'device/mybooking.html',{'order_list' : order_list})
