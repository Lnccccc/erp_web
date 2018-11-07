from django import forms
from django.contrib.admin import widgets
from .models import orders_list
from datetime import datetime
class WorkFlowForm(forms.ModelForm):
    order_time = forms.DateField()
    sub_time = forms.DateField(widget=widgets.AdminDateWidget())
    order_time.widget.attrs.update({'value':str(datetime.now())})
    client = forms.CharField(max_length=256)
    order_quantity = forms.IntegerField()
    spec = forms.CharField(max_length=256)
    unit = forms.CharField(max_length=256)
    person_incharge = forms.CharField(max_length=256)
    client.widget.attrs.update({'class':'form-control','id':'focusedInput'})
    order_quantity.widget.attrs.update({'class':'form-control','id':'focusedInput'})
    spec.widget.attrs.update({'class':'form-control','id':'focusedInput'})
    unit.widget.attrs.update({'class':'form-control','id':'focusedInput'})
    person_incharge.widget.attrs.update({'class':'form-control','id':'focusedInput'})

    class Meta:
        model=orders_list



