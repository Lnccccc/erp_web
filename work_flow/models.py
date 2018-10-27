from django.db import models
from django.contrib.admin import widgets
# Create your models here.

class orders_list(models.Model):
    user_name = models.CharField(max_length=200,null=True)
    uuid = models.CharField(max_length=200,null=True)
    client = models.CharField(max_length=200,null=True)
    order_time = models.DateField()
    sub_time = models.DateField()
    order_num = models.CharField(max_length=200,null=True)
    order_detail = models.CharField(max_length=200,null=True)
    ps = models.CharField(max_length=200)
    order_status = models.IntegerField()
    person_incharge = models.CharField(max_length=100)

class order_stat(models.Model):
    stat_cd = models.IntegerField(primary_key=True)
    stat_nam = models.CharField(max_length=100)

class charge_person(models.Model):
    person_cd = models.CharField(max_length=200)
    person_nam = models.CharField(max_length=200)






