from django import forms
from django.contrib.admin import widgets
from .models import orders_list
from datetime import datetime
class WorkFlowForm(forms.ModelForm):
    class Meta:
        model = orders_list
        fields = ('client','order_num','order_detail','ps','person_incharge')
    # client = forms.CharField(max_length=200)
    order_time = forms.DateField()
    sub_time = forms.DateField(widget=widgets.AdminDateWidget())
    order_time.widget.attrs.update({'value':str(datetime.now())})


