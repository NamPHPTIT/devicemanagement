from django.urls import path
from .views import views
from .views.devices import control,edit
from .views.order import confirm,giveback,order_edit,preorder

urlpatterns = [
    path('404', views.handle404, name='404'),
    path('', control.list_all, name = 'list_all'),
    path('pages=<int:page>', control.list_page, name = 'pages'),
    path('function=<slug:function>', control.list_function, name = 'function'),
    # path('search/',views.search, name = 'search'),
    path('detail/<slug:device_code>/', views.detail, name = 'detail'),
    path('add/',edit.add_device, name = 'add_device'),
    path('edit/',edit.edit_device, name = 'edit_device'),
    path('order/add/<slug:device_code>%<slug:username>/',views.preorder, name = 'preorder'),
    path('order/add/',views.order_add, name = 'order_add'),
    path('supplement/add/',views.sup_add, name = 'sup_add'),
    path('supplement/add/<slug:username>/',views.presup, name = 'presup'),
    path('mybooking/<slug:username>',views.mybooking, name = 'mybooking'),
    path('update/giveback/',giveback.listgiveback, name = 'listgiveback'),
    path('update/giveback/<int:id>',giveback.updategiveback, name = 'updategiveback'),
    path('mybooking/<slug:username>/<int:id>/',giveback.giveback, name = 'giveback'),
    path('confirm/<int:id>/',confirm.updateconfirm, name = 'confirmbooked'),
    path('confirm/rejected/<int:id>/',confirm.updateconfirm, name = 'confirmbooked'),
    path('confirm/',confirm.listconfirm, name = 'confirm'),
    path('project/',views.preaddproject, name ='pre_add_project'),
    path('project/add/',views.addproject, name ='add_project'),
]
