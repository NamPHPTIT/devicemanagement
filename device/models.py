from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    code = models.CharField(max_length=15, unique = True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    ostype = models.CharField(max_length=15)
    version = models.CharField(max_length=10)
    status = models.CharField(max_length=10)

class Department(models.Model):
    name = models.CharField(max_length=15, unique = True)
    account =  models.ManyToManyField(User)

class Project(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    account = models.ManyToManyField(User)

class Order(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    fromdate = models.DateTimeField()
    todate = models.DateTimeField()
    givebackdate = models.DateTimeField()
    orderstatus =  models.CharField(max_length=10)
    reason = models.TextField()

class Supplement(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="quantity")
    requestdate = models.DateTimeField()
    receivedate = models.DateTimeField()
    status =  models.CharField(max_length=10)
    reason = models.TextField()
