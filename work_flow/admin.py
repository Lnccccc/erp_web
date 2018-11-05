from django.contrib import admin
from .models import orders_list,order_stat,charge_person
admin.site.register(orders_list)
admin.site.register(order_stat)
admin.site.register(charge_person)
# Register your models here.
