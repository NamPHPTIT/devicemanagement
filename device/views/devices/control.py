from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from device.models import Device,Order,Project,Supplement,Department
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q,F,Count
import datetime

device_list = Device.objects.prefetch_related('order_set')\
.values('code').annotate(c = Count('code'))\
.filter(~Q(status='Booked')|Q(order__orderstatus='Borrowed'))\
.values('code', 'name','order__fromdate','order__todate', 'order__reason','order__account__username','type', 'ostype', 'version', 'status','order__orderstatus')\
.order_by('code')

overdue_count = Order.objects.filter(givebackdate = None).exclude(todate__gt = datetime.date.today()).count

d = Device.objects.all()
def list_all(request):
    if request.method == 'POST':
        if request.POST['search']:
            if device_list.filter(code = request.POST['search']):
                return render(request, 'device/listall.html',{'devices' : device_list.filter(code = request.POST['search'])[:5],'device_count' :d.count,'free_count' :d.filter(status='Free').count,'booked_count' :d.filter(status='Booked').count ,'overdue_count' :overdue_count})
            else:
                return render(request, 'device/listall.html',{'devices' : device_list.filter(name__contains = request.POST['search'])[:5],'device_count' :d.count,'free_count' :d.filter(status='Free').count,'booked_count' :d.filter(status='Booked').count,'overdue_count' :overdue_count})
        else :
            return render(request, 'device/listall.html',{'devices' : device_list[:5],'device_count' :d.count,'free_count' :d.filter(status='Free').count,'booked_count' :d.filter(status='Booked').count,'overdue_count' :overdue_count})
    else:
        return render(request, 'device/listall.html',{'devices' : device_list[:5],'device_count' :d.count,'free_count' :d.filter(status='Free').count,'booked_count' :d.filter(status='Booked').count,'overdue_count' :overdue_count})

def list_page(request,page):
        return render(request, 'device/listall.html',{'devices' : device_list[((page-1)*5):page*5],'device_count' :d.count,'free_count' :d.filter(status='Free').count,'booked_count' :d.filter(status='Booked').count,'overdue_count' :overdue_count})

def list_function(request,function):
    # if function == 'overdue':
    #     return render(request, 'device/listall.html',{'devices' : device_list.filter(order__givebackdate = None).exclude(order__todate__gt = datetime.date.today())})
    # else :
        return render(request, 'device/listall.html',{'devices' : device_list.filter(status = function),'device_count' :d.count,'free_count' :d.filter(status='Free').count,'booked_count' :d.filter(status='Booked').count,'overdue_count' :overdue_count})
