from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from device.models import Device,Order,Project,Supplement,Department
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q,F,Count
import datetime

device_list = Device.objects.prefetch_related('order_set')\
.values('code').annotate(c = Count('code'))\
.values('code', 'name', 'c','order__fromdate', 'order__reason','order__account__username','type', 'ostype', 'version', 'status','order__orderstatus')\
.order_by('code')
# .filter(Q(status = 'Free')|~Q(order__orderstatus = 'Completed'))\
# .values('code', 'name', 'type', 'ostype', 'version', 'status', 'order__fromdate', 'order__todate','order__givebackdate','order__orderstatus', 'order__reason', 'order__account__username', 'order__project__name','c')\


overdue_count = Order.objects.filter(givebackdate = None).exclude(todate__gt = datetime.date.today()).count

#device_list = Device.objects.raw('''SELECT * FROM devicemanager.device_device left join devicemanager.device_order on device_device.id = device_id group by code''')

def is_member(user):
    return user.groups.filter(name='bridge_engineer').exists()

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url="/accounts/login")
def detail(request, device_code):
    device = get_object_or_404(Device, code=device_code)
    return render(request, 'device/detail.html',{'device' : device})

@login_required(login_url="/accounts/login")
def preorder(request, device_code,username):
    projects = Project.objects.filter(account__username = username )
    device = get_object_or_404(Device, code=device_code)
    ctx = { 'device': device, 'projects': projects }
    return render(request, 'order/order_add.html',ctx)

def handle404(request):
    return render(request, 'device/404.html')

@login_required(login_url="/accounts/login")
def preaddproject(request):
    departments = Department.objects.all()
    user = User.objects.all()
    ctx = { 'departments': departments, 'accounts': user }
    return render(request, 'project/project_add.html',ctx)

#GIVEBACK
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

#CONFIRM BOOKED
@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url = '/device/404')
def updateconfirm(request, id):
    order = get_object_or_404(Order, id=id)
    order.device.status = 'Booked'
    order.device.save()
    order.orderstatus = 'Borrowed'
    order.save()
    order_list = Order.objects.all().filter(orderstatus = 'ORequest')
    return render(request, 'order/order_confirm.html',{'order_list' : order_list})

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url = '/device/404')
def listconfirm(request):
    order_list = Order.objects.all().filter(orderstatus = 'ORequest')
    return render(request, 'order/order_confirm.html',{'order_list' : order_list})

#PRE SUPPLEMENT
@login_required(login_url="/accounts/login")
def presup(request,username):
    projects = Project.objects.filter(account__username = username )
    return render(request, 'supplement/sup_add.html',{'projects': projects})

@login_required(login_url="/accounts/login")
def mybooking(request,username):
    order_list = Order.objects.filter(account__username = username )
    return render(request, 'device/mybooking.html',{'order_list' : order_list})

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

@login_required(login_url="/accounts/login")
def order_add(request):
    if request.method == 'POST':
        if request.POST['project'] and request.POST['username'] and request.POST['devicecode'] and request.POST['fromdate'] and request.POST['todate'] and request.POST['reason']:
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

@login_required(login_url="/accounts/login")
@user_passes_test(is_member,login_url = '/device/404')
def sup_add(request):
    if request.method == 'POST':
        if request.POST['project'] and request.POST['username'] and request.POST['devicename'] and request.POST['devicetype'] and request.POST['ostype'] and request.POST['version'] and request.POST['quantity'] and request.POST['reason']:
            sup = Supplement()
            project = get_object_or_404(Project,name = request.POST['project'])
            user = get_object_or_404(User, username = request.POST['username'])

            device = Device()
            device.code = ''
            device.name = request.POST['devicename']
            device.type = request.POST['devicetype']
            device.ostype = request.POST['ostype']
            device.version = request.POST['version']
            device.status = 'Ordered'

            sup.account = user
            sup.project = project
            sup.device = device
            sup.status = 'Requesting'
            sup.quantity = request.POST['quantity']
            sup.reason = request.POST['reason']
            sup.save()
            return redirect('http://localhost:8000/device/')
        else:
            return render(request, 'supplement/sup_add.html',{'error':'All fields are required.'})
    else:
        return render(request, 'supplement/sup_add.html')

@login_required(login_url="/accounts/login")
@user_passes_test(lambda u: u.is_superuser,login_url="/accounts/login")
def addproject(request):
    departments = Department.objects.all()
    user = User.objects.all()
    if request.method == 'POST':
        if request.POST['name'] and request.POST['department'] and request.POST['accounts']:
            try:
                project = Project()
                project.name = request.POST['name']
                department = get_object_or_404(Department, id=request.POST['department'] )
                project.department = department
                project.save()
                accounts = request.POST.getlist('accounts')
                for acc in accounts:
                    project.account.add( User.objects.get(username=acc))
                project.save()
                return redirect('http://localhost:8000/device/')
            except:
                ctx = { 'departments': departments, 'accounts': accounts ,'error':'Something Wrong!'}
                return render(request, 'project/project_add.html',ctx)
        else:
            ctx = { 'departments': departments, 'accounts':accounts ,'error':'All fields are required.'}
            return render(request, 'project/project_add.html',ctx)
    else:
        return render(request, 'project/project_add.html')
