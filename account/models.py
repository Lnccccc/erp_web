from django.db import models
from django.conf import settings

# Create your models here.

class WeixinUser(models.Model):
    openid = models.CharField(max_length=256,null=True)
    nickname = models.CharField(max_length=256,null=True)
    sex = models.CharField(max_length=256,null=True)
    city = models.CharField(max_length=256,null=True)

class Profile(models.Model):
    dept_list = (('总经理','总经理'),('厂长','厂长'),('生产主管','生产主管'),('仓管','仓管'),('空','空'))
    user = models.OneToOneField(WeixinUser,on_delete=models.CASCADE)
    company = models.CharField(max_length=200,null=True,default='空')
    dept = models.CharField(max_length=200,null=True,choices=dept_list,default='空')
    realname = models.CharField(max_length=256,null=True,default='空')

    def __str__(self):
        return 'Profile for user {}'.format(self.user.nickname)

