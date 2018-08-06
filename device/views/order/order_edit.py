from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from device.models import Device,Order,Project,Supplement,Department
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q,F,Count
import datetime

@login_required(login_url="/accounts/login")
def mybooking(request,username):
    order_list = Order.objects.filter(account__username = username )
    return render(request, 'device/mybooking.html',{'order_list' : order_list})

@login_required(login_url="/accounts/login")
def order_add(request):
    if request.method == 'POST':
        if request.POST['project'] and request.POST['username'] and request.POST['devicecode'] and request.POST['fromdate'] and request.POST['todate'] and request.POST['reason']:
            # delta = request.POST['todate'] - request.POST['fromdate']
            # if delta.days > 60:
            #     return render(request, 'order/order_add.html',{'error':'Order max is 60 days.'})
            # else:
                order = Order()
                project = get_object_or_404(Project,id = request.POST['project'])
                acc = get_object_or_404(User, username = request.POST['username'])
                device = get_object_or_404(Device, code = request.POST['devicecode'])
                order.account = acc
                order.project = project
                order.device = device
                order.fromdate = request.POST['fromdate']
                order.todate = request.POST['todate']
                order.reason = request.POST['reason']
                order.orderstatus = "ORequest"
                order.save()
                return redirect('http://localhost:8000/device/')
        else:
            return render(request, 'order/order_add.html',{'error':'All fields are required.'})
    else:
        return render(request, 'order/order_add.html')
