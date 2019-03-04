from django.db import models
from django.conf import settings

# Create your models here.

class WeixinUser(models.Model):
    openid = models.CharField(max_length=256,null=True)
    nickname = models.CharField(max_length=256,null=True)
    sex = models.CharField(max_length=256,null=True)
    city = models.CharField(max_length=256,null=True)
    def __str__(self):
        return self.nickname

class Company(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True,default="示例企业")
    owner = models.CharField(max_length=200,blank=True,null=True)
    db = models.CharField(max_length=100,blank=True,null=True)
    driver = models.CharField(max_length=100,blank=True,null=True)
    user = models.CharField(max_length=100,blank=True,null=True)
    passwd = models.CharField(max_length=100,blank=True,null=True)
    host = models.IPAddressField()
    port = models.IntegerField(max_length=50,blank=True,null=True)
    schema = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return self.name
    

class Profile(models.Model):
    dept_list = (('总经理','总经理'),('厂长','厂长'),('生产主管','生产主管'),('仓管','仓管'),('空','空'))
    user = models.OneToOneField(WeixinUser,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,related_name='membs',on_delete=models.CASCADE,null=True,blank=True,default=1)
    dept = models.CharField(max_length=200,null=True,choices=dept_list,default='总经理')
    realname = models.CharField(max_length=256,null=True,default='空')

    def __str__(self):
        return self.realname


class Access_Token(models.Model):
    token = models.CharField(max_length=512,blank=True)
    expires = models.IntegerField(blank=True)
