from django.db import models
from django.conf import settings

# Create your models here.

class WeixinUser(models.Model):
    openid = models.CharField(max_length=256,null=True)
    nickname = models.CharField(max_length=256,null=True)
    sex = models.CharField(max_length=256,null=True)
    city = models.CharField(max_length=256,null=True)

class Company(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    owner = models.CharField(max_length=200,null=True,blank=True)
    class Meta:
        def __str__(self):
            return "%s,%s" %(self.name,self.owner)

class Profile(models.Model):
    dept_list = (('总经理','总经理'),('厂长','厂长'),('生产主管','生产主管'),('仓管','仓管'),('空','空'))
    user = models.OneToOneField(WeixinUser,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,default='示例企业')
    dept = models.CharField(max_length=200,null=True,choices=dept_list,default='空')
    realname = models.CharField(max_length=256,null=True,default='空')
    def __str__(self):
        return 'Profile for user {}'.format(self.user.nickname)

