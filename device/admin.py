from django.contrib import admin
from .models import Device,Order,Project,Supplement,Department
# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['code','name','type','ostype','version','status']
    search_fields = ['code','name']

admin.site.register(Device,DeviceAdmin)
admin.site.register(Order)
admin.site.register(Project)
admin.site.register(Supplement)
admin.site.register(Department)
