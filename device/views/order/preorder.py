from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from device.models import Device,Order,Project,Supplement,Department
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q,F,Count
import datetime

@login_required(login_url="/accounts/login")
def preorder(request, device_code,username):
    projects = Project.objects.filter(account__username = username )
    device = get_object_or_404(Device, code=device_code)
    ctx = { 'device': device, 'projects': projects }
    return render(request, 'order/order_add.html',ctx)
