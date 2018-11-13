from django.db import models
from django.contrib.admin import widgets
import datetime
# Create your models here.

class orders_list(models.Model):
    openid = models.CharField(max_length=256,null=True)
    user_name = models.CharField(max_length=200,null=True)
    uuid = models.CharField(max_length=200,null=True)
    client = models.CharField(max_length=200,null=True)
    order_time = models.DateField()
    sub_time = models.DateField()
    order_quantity = models.IntegerField(null=True) #数量
    spec = models.CharField(max_length=200,null=True) #规格
    unit = models.CharField(max_length=200) ##单位
    order_status = models.IntegerField()
    person_incharge = models.CharField(max_length=100)
    company = models.CharField(max_length=256,null=True)
    requirement = models.CharField(max_length=256,null=True,default='暂无') #用纸要求
    remark = models.CharField(max_length=256,null=True,default='暂无') #备注

class order_stat(models.Model):
    stat_cd = models.IntegerField(primary_key=True)
    stat_nam = models.CharField(max_length=100)

class charge_person(models.Model):
    person_cd = models.CharField(max_length=200)
    person_nam = models.CharField(max_length=200)






