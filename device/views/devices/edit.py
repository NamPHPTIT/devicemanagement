from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from device.models import Device,Order,Project,Supplement,Department
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q,F,Count
import datetime

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url="/accounts/login")
def detail(request, device_code):
    device = get_object_or_404(Device, code=device_code)
    return render(request, 'device/detail.html',{'device' : device})

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url = '/device/404')
def add_device(request):
    if request.method == 'POST':
        if request.POST['code'] and request.POST['name'] and request.POST['type'] and request.POST['ostype'] and request.POST['version'] and request.POST['status']:
            try:
                device = Device()
                device.code = request.POST['code']
                device.name = request.POST['name']
                device.type = request.POST['type']
                device.ostype = request.POST['ostype']
                device.version = request.POST['version']
                device.status = request.POST['status']
                device.save()
                #return redirect('/device/detail/' + str(device.code))
                return render(request, 'device/add.html',{'device':device})
            except:
                return render(request, 'device/add.html',{'error':'Something Wrong!'})
        else:
            return render(request, 'device/add.html',{'error':'All fields are required.'})
    else:
        return render(request, 'device/add.html')

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url = '/device/404')
def edit_device(request):
    if request.method == 'POST':
        if request.POST['code'] and request.POST['name'] and request.POST['type'] and request.POST['ostype'] and request.POST['version'] and request.POST['status']:
            device = get_object_or_404(Device, code = request.POST['code'])
            device.name = request.POST['name']
            device.type = request.POST['type']
            device.ostype = request.POST['ostype']
            device.version = request.POST['version']
            device.status = request.POST['status']
            device.save()
            return redirect('/device/detail/' + str(device.code))
        else:
            return render(request, 'device/detail.html',{'error':'All fields are required.'})
    else:
        return render(request, 'device/detail.html')
