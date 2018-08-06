from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from device.models import Device,Order,Project,Supplement,Department
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q,F,Count
import datetime

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url = '/device/404')
def updateconfirm(request, id):
    order = get_object_or_404(Order, id=id)
    order.device.status = 'Booked'
    order.device.save()
    order.orderstatus = 'Borrowed'
    order.save()
    for o in Order.objects.all().filter(orderstatus = 'ORequest').filter(device__code = order.device.code ):
        o.orderstatus = 'Rejected'
        o.save()
    order_list = Order.objects.all().filter(orderstatus = 'ORequest')
    return render(request, 'order/order_confirm.html',{'order_list' : order_list})

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url = '/device/404')
def rejected(request, id):
    order = get_object_or_404(Order, id=id)
    order.orderstatus = 'Rejected'
    order.save()
    order_list = Order.objects.all().filter(orderstatus = 'ORequest')
    return render(request, 'order/order_confirm.html',{'order_list' : order_list})

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url = '/device/404')
def listconfirm(request):
    order_list = Order.objects.all().filter(orderstatus = 'ORequest')
    return render(request, 'order/order_confirm.html',{'order_list' : order_list})
