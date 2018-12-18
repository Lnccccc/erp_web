from django.contrib import admin
from .models import Profile,WeixinUser,Company

# Register your models here.
admin.site.register(Profile)
admin.site.register(WeixinUser)
admin.site.register(Company)
