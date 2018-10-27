from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    dept_list = (('总经理','总经理'),('厂长','厂长'),('生产主管','生产主管'),('仓管','仓管'),('空','空'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    company = models.CharField(max_length=200,null=True,default='空')
    dept = models.CharField(max_length=200,null=True,choices=dept_list,default='空')

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

